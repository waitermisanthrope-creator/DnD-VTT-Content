using System;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using DndVtt.UnityPrototype;
static class WorldChecks
{
 public static void Run(string source)
 {
  int count=0;
  void Check(bool ok,string message){if(!ok)throw new Exception(message);count++;}
  void Reject(Action action,string message){bool rejected=false;try{action();}catch(FormatException){rejected=true;}Check(rejected,message);}
  var catalog=WorkshopStore.Catalog(File.ReadAllText(Path.Combine(source,"catalog/v3/index.json")),"packages");
  var manifests=catalog.OfType<JObject>().Where(m=>(string)m["worldLootRevision"]=="1.0.0").ToArray();
  Check(manifests.Length==25,"25 optional expansion packages");
  string root=Path.Combine(Path.GetTempPath(),"world-loot-"+Guid.NewGuid());Directory.CreateDirectory(root);
  try {
   string FileFor(JObject m)=>Path.Combine(source,"packages",Path.GetFileName((string)m["url"]));
   void Install(WorkshopStore store,JObject m,string platform="android-arm64") {string download=Path.Combine(root,"download.json");File.Copy(FileFor(m),download,true);store.Install(m,download,platform,"6000.3.26f1");}
   var rulesManifest=catalog.OfType<JObject>().First(m=>(string)m["id"]=="dnd.alchemy.rules");
   var combined=new WorkshopStore(Path.Combine(root,"combined"));
   Check(combined.Installed().Count==0,"optional startup installs nothing");
   foreach(var m in manifests) {
    var data=WorkshopStore.ValidateData(m,File.ReadAllText(FileFor(m)));Check(data!=null,"published runtime accepts payload");
    foreach(string platform in new[]{"android-arm64","windows-x64"}) {
     var isolated=new WorkshopStore(Path.Combine(root,(string)m["id"]+platform));
     if((string)m["type"]=="craft") {
      Reject(()=>Install(isolated,m,platform),"profiles require separately installed alchemy rules");
      Check(isolated.Installed().Count==0,"failed dependency check installs nothing");
      Install(isolated,rulesManifest,platform);
     }
     Install(isolated,m,platform);
     var restart=new WorkshopStore(isolated.Root);
     Check(restart.Find((string)m["id"])!=null,"restart installation "+platform);
     Check(((JArray)restart.Commerce()["items"]).Count==((JArray)data["items"]).Count,"only selected optional items active");
     isolated.Remove((string)m["id"]);Check(isolated.Find((string)m["id"])==null,"optional remove");
    }
    if((string)m["type"]=="item")Install(combined,m);
   }
   Check(((JArray)combined.Commerce()["items"]).Count==464,"464 new functional records");
   Check(((JArray)combined.Commerce()["alchemy"]["ingredients"]).Count==0,"profiles are optional separately");
   var butter=((JArray)combined.Commerce()["items"]).OfType<JObject>().Single(i=>(string)i["name"]=="Нож для масла");
   Check((string)butter["inventoryCategory"]=="weapons" && ((JArray)butter["itemTraits"]["uses"]).Any(u=>(string)u["action"]=="cut_soft_food"),"butter knife cuts soft food as manual affordance");
   var goblin=((JArray)combined.Commerce()["items"]).OfType<JObject>().Single(i=>(string)i["name"]=="Селезёнка гуманоида");
   Check((string)goblin["alchemyId"]=="harvest_humanoid_spleen" && goblin["properties"]==null,"generic spleen links research without leaking effects in item");
   var hero=JObject.Parse("{id:'goblin-loot',name:'Explorer',ac:14,hpCurrent:5,hpMax:20,proficiencies:['p_tool_alchemist'],unknown:{keep:true}}");
   var sample=(JObject)goblin.DeepClone();sample["itemTraits"]["provenance"]=JObject.Parse("{creatureName:'Гоблин',harvesterId:'test'}");
   CommerceRules.AddItem(hero,sample,2);CommerceRules.AddItem(hero,butter);var knife=(JObject)hero["inventory"]["weapons"][0];CommerceRules.Equip(hero,knife);
   Check((bool)knife["equipped"]&&(int)hero["ac"]==14,"household knife really equips using existing runtime");
   Install(combined,rulesManifest);
   foreach(var m in manifests.Where(m=>(string)m["type"]=="craft"))Install(combined,m);
   // Material volumes provide the 54 existing canonical parts; none are duplicated by this expansion.
   foreach(var m in catalog.OfType<JObject>().Where(m=>m["collectionVolume"]!=null))Install(combined,m);
   var commerce=combined.Commerce();var items=(JArray)commerce["items"];var alchemy=(JObject)commerce["alchemy"];
   Check(items.Count==3755,"old 3291 volumes plus 464 without replacement");
   Check(items.OfType<JObject>().Select(i=>(string)i["id"]).Distinct().Count()==items.Count,"no duplicate item IDs");
   Check(((JArray)alchemy["ingredients"]).Count==219,"219 generic part profiles");
   Check(hero["alchemyState"]==null,"spleen properties initially unknown");
   CommerceRules.Research(hero,alchemy,"harvest_humanoid_spleen");
   Check(((JArray)hero["alchemyState"]["discovered"]["harvest_humanoid_spleen"]).Count==1,"research really discovers one property");
   Check((int)hero["inventory"]["materials"][0]["count"]==2,"research retains specimen");
   Check((string)hero["inventory"]["materials"][0]["name"]=="Селезёнка гуманоида" && (string)hero["inventory"]["materials"][0]["itemTraits"]["provenance"]["creatureName"]=="Гоблин","source recorded separately from generic item name");
   Check(JToken.DeepEquals(new LegacyCharacterArchive(new LegacyCharacterArchive(hero.ToString()).Export()).Snapshot(0),hero),"traits provenance and discovered property survive archive roundtrip");
   var secondHero=JObject.Parse("{id:'another',name:'Another'}");CommerceRules.AddItem(secondHero,sample);
   Check(secondHero["alchemyState"]==null,"knowledge belongs to character not global item");
   foreach(JObject profile in (JArray)alchemy["ingredients"]) {
    var ingredient=items.OfType<JObject>().First(i=>(string)i["alchemyId"]==(string)profile["id"] || (string)i["name"]==(string)profile["name"]);
    var actor=JObject.Parse("{id:'research',name:'Researcher',proficiencies:['p_tool_alchemist']}");CommerceRules.AddItem(actor,ingredient,2);
    string id=(string)profile["id"];
    foreach(var property in (JArray)profile["properties"])CommerceRules.Research(actor,alchemy,id);
    Check(JToken.DeepEquals(actor["alchemyState"]["discovered"][id],profile["properties"]),"all properties actually researchable: "+id);
    string before=actor.ToString();Reject(()=>CommerceRules.Research(actor,alchemy,id),"fully researched rejects without invented property");Check(before==actor.ToString(),"completed research atomic");
    Check((bool)CommerceRules.Mix(actor,alchemy,new[]{id,id},null,100)["ok"],"actual alchemy recipe resolves: "+id);
    Check(((JArray)actor["inventory"]["materials"]).Count==0,"mix consumes two generic samples");
    before=actor.ToString();Reject(()=>CommerceRules.Mix(actor,alchemy,new[]{id,id},null,100),"no sample double spend");Check(before==actor.ToString(),"failed mix preserves full state");
   }
   foreach(var item in items.OfType<JObject>().Where(i=>((string)i["id"]).StartsWith("dnd.items.world.")&&(string)i["inventoryCategory"]=="consumables")) {
    var actor=JObject.Parse("{id:'manual',name:'User',hpCurrent:3,hpMax:20}");CommerceRules.AddItem(actor,item,2);var dose=(JObject)actor["inventory"]["consumables"][0];CommerceRules.UseProduct(actor,dose);
    Check((int)dose["count"]==1&&(int)actor["hpCurrent"]==3,"supplies consume stock without fictional automatic effect");
   }
   string saved=hero.ToString();combined.Remove((string)manifests.First(m=>(string)m["worldLootFamily"]=="anatomy.humanoid")["id"]);
   Check(hero.ToString()==saved,"uninstall does not change owned specimen or knowledge");
   Check((bool)hero["unknown"]["keep"],"unknown character fields preserved");
  } finally {Directory.Delete(root,true);}
  Console.WriteLine("WORLD_LOOT_COMPATIBILITY_PASS "+count+" checks; published pure runtime, Android/Windows contracts; no physical GUI claim");
 }
}
