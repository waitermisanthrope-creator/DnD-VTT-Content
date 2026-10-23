using System;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using DndVtt.UnityPrototype;
class Compatibility
{
 static int checks;
 static void Check(bool ok,string name) {if(!ok)throw new Exception(name);checks++;}
 static void Main(string[] args)
 {
  string source=Path.GetFullPath(args[0]);
  var catalog=WorkshopStore.Catalog(File.ReadAllText(Path.Combine(source,"catalog/v3/index.json")),"packages");
  var volumes=catalog.OfType<JObject>().Where(m=>m["collectionVolume"]!=null).ToArray();
  Check(volumes.Length==36,"36 optional volumes");
  string root=Path.Combine(Path.GetTempPath(),"published-workshop-"+Guid.NewGuid());Directory.CreateDirectory(root);
  try {
   var combined=new WorkshopStore(Path.Combine(root,"all"));
   Check(((JArray)combined.Commerce()["items"]).Count==0,"nothing installed by default");
   foreach(var m in volumes) {
    string file=Path.Combine(source,"packages",Path.GetFileName((string)m["url"]));
    var data=WorkshopStore.ValidateData(m,File.ReadAllText(file));
    Check(((JArray)data["items"]).Count<=100,"old client 100 item bound");
    Check(((JArray)m["dependencies"]).Count==0,"independent volume");
    Check(((JArray)data["items"]).OfType<JObject>().All(i=>i["weight"]!=null&&!string.IsNullOrWhiteSpace((string)i["description"])),"weight/description");
    foreach(string platform in new[]{"android-arm64","windows-x64"}) {
     var isolated=new WorkshopStore(Path.Combine(root,(string)m["id"]+platform));
     string download=Path.Combine(root,"download.json");File.Copy(file,download,true);isolated.Install(m,download,platform,"6000.3.26f1");
     var restarted=new WorkshopStore(isolated.Root);
     Check(restarted.Installed().Count==1,"only selected volume installed");
     Check(((JArray)restarted.Commerce()["items"]).Count==((JArray)data["items"]).Count,"activation/restart "+platform);
     isolated.Remove((string)m["id"]);Check(isolated.Installed().Count==0,"optional uninstall");
    }
    string part=Path.Combine(root,"download.json");File.Copy(file,part,true);combined.Install(m,part,"android-arm64","6000.3.26f1");
   }
   var items=(JArray)combined.Commerce()["items"];Check(items.Count==3291,"all 3291 library records");
   Check(items.OfType<JObject>().Select(i=>(string)i["id"]).Distinct().Count()==items.Count,"no duplicate inventory IDs");
   var hero=JObject.Parse("{id:'compatibility',name:'Test',hpCurrent:1,hpMax:100,stats:{dex:10},ac:12,unknown:{keep:true}}");
   foreach(var item in items.OfType<JObject>().Where(i=>(string)i["inventoryCategory"]=="consumables")) {
    int before=(int)hero["hpCurrent"];CommerceRules.AddItem(hero,item,2);var dose=(JObject)((JArray)hero["inventory"]["consumables"]).Last();
    CommerceRules.UseProduct(hero,dose);Check((int)dose["count"]==1,"every consumable spends exactly one dose");
    if((string)item["id"] is string id && id.Contains("healing.")) {
     int amount=(int)item["potency"]/10;Check((int)hero["hpCurrent"]==Math.Min(100,before+amount),"actual existing-client healing amount");
    }
    else Check((int)hero["hpCurrent"]==before,"manual consumable makes no unsupported HP change");
    CommerceRules.UseProduct(hero,dose);Check(((JArray)hero["inventory"]["consumables"]).Count==0,"empty stock removed");hero["hpCurrent"]=1;
   }
   var weapon=items.OfType<JObject>().First(i=>(string)i["inventoryCategory"]=="weapons");CommerceRules.AddItem(hero,weapon);
   var owned=(JObject)hero["inventory"]["weapons"][0];CommerceRules.Equip(hero,owned);Check((bool)owned["equipped"],"weapon equip");
   var armor=items.OfType<JObject>().First(i=>(string)i["inventoryCategory"]=="armor"&&(double?)i["acBase"]>0);CommerceRules.AddItem(hero,armor);
   owned=(JObject)hero["inventory"]["armor"][0];CommerceRules.Equip(hero,owned);Check((bool)owned["equipped"]&&(int)hero["ac"]>=10,"armor equip and AC");
   Check(JToken.DeepEquals(new LegacyCharacterArchive(new LegacyCharacterArchive(hero.ToString()).Export()).Snapshot(0),hero),"existing save roundtrip");
   Check((bool)hero["unknown"]["keep"],"unknown save fields retained");
   // Existing ingredient packages remain optional and retain their original chemistry.
   foreach(var m in catalog.OfType<JObject>().Where(m=>(string)m["id"]=="dnd.alchemy.rules" || ((string)m["id"]).StartsWith("dnd.alchemy.ingredients."))) {
    string part=Path.Combine(root,"download.json");File.Copy(Path.Combine(source,"packages",Path.GetFileName((string)m["url"])),part,true);combined.Install(m,part,"android-arm64","6000.3.26f1");
   }
   Check(((JArray)combined.Commerce()["items"]).Count==3411,"existing 120 ingredients do not duplicate volumes");
   Check(((JArray)combined.Commerce()["alchemy"]["ingredients"]).Count==120,"existing chemistry preserved");
   var invalid=(JObject)WorkshopStore.Parse(File.ReadAllText(Path.Combine(source,"packages",Path.GetFileName((string)volumes[0]["url"])))).DeepClone();
   ((JArray)invalid["items"]).Add(((JArray)invalid["items"])[0].DeepClone());bool rejected=false;
   try{WorkshopStore.ValidateData(volumes[0],invalid.ToString());}catch(FormatException){rejected=true;}Check(rejected,"old 100-entry bound genuinely enforced");
   foreach(var category in new[]{"weapons","armor","materials","consumables","junk"}) {
    var old=JObject.Parse(File.ReadAllText(Path.Combine(source,"packages","dnd.items."+category+".json")));
    Check(((JArray)old["items"]).All(i=>items.Any(n=>(string)n["id"]==(string)i["id"])),"original stable IDs retained "+category);
   }
  } finally {Directory.Delete(root,true);}
  Console.WriteLine("PUBLISHED_CLIENT_COMPATIBILITY_PASS "+checks+" checks; Android/Windows pure runtime, no device GUI claim");
 }
}
