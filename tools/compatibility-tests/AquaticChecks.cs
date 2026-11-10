using System;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using DndVtt.UnityPrototype;
static class AquaticChecks {
 static int checks;
 static void Check(bool ok,string name){if(!ok)throw new Exception(name);checks++;}
 public static void Run(string root){
  checks=0;var manifests=WorkshopStore.Catalog(File.ReadAllText(Path.Combine(root,"catalog/v3/index.json")),"packages");
  string[] pids={"dnd.race.kuo_toa","dnd.race.merrow","dnd.race.triton","dnd.race.sahuagin","dnd.race.locathah"};
  Check(pids.All(id=>manifests.Any(m=>(string)m["id"]==id)),"all five races must exist in workshop");
  JObject Find(string id)=>manifests.OfType<JObject>().Single(m=>(string)m["id"]==id);
  string Payload(JObject m)=>Path.Combine(root,"packages",Path.GetFileName((string)m["url"]));
  var cls=(JObject)JObject.Parse(File.ReadAllText(Path.Combine(root,"packages/dnd.class.blood_hunter.json")))["classes"][0];
  var bg=JObject.Parse("{name:'Test background',seed:{},choices:[]}");
  var stats=JObject.Parse("{str:10,dex:10,con:10,int:10,wis:10,cha:10}");
  foreach(var platform in new[]{"android-arm64","windows-x64"}){
   string tmp=Path.Combine(Path.GetTempPath(),"aquatic-"+Guid.NewGuid());Directory.CreateDirectory(tmp);
   try{
    var store=new WorkshopStore(Path.Combine(tmp,"store"));
    void Install(JObject m){string download=Path.Combine(tmp,"download.json");File.Copy(Payload(m),download,true);store.Install(m,download,platform,"6000.3.26f1");}
    var legacy=JObject.Parse(File.ReadAllText(Path.Combine(root,"packages/dnd.race.triton.json")));
    var old=(JObject)Find("dnd.race.triton").DeepClone();old["version"]="1.0.0";
    var raw=File.ReadAllBytes(Path.Combine(root,"packages/dnd.race.triton.json"));old["bytes"]=raw.Length;old["sha256"]=Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(raw)).ToLowerInvariant();
    File.WriteAllBytes(Path.Combine(tmp,"old.json"),raw);store.Install(old,Path.Combine(tmp,"old.json"),platform,"6000.3.26f1");
    foreach(var id in pids)Install(Find(id));
    var collection=Find("dnd.collections.aquatic-races");WorkshopStore.ValidateData(collection,File.ReadAllText(Payload(collection)));Install(collection);
    Check(WorkshopStore.InstallPlan(collection,manifests.OfType<JObject>(),Array.Empty<JObject>(),platform,"6000.3.26f1",10040).Count==6,"theme plan includes all five races and collection");
    var all=Find("dnd.collections.races");WorkshopStore.ValidateData(all,File.ReadAllText(Payload(all)));
    Check(((JArray)all["dependencies"]).Count==47,"full race library updated");
    store=new WorkshopStore(store.Root);
    var catalog=store.Creation(JObject.Parse("{races:[],classes:[],feats:[],proficiencies:[]}"));
    Check(((JArray)catalog["races"]).Count==5,"only five unique races after upgrade and restart");
    foreach(JObject race in (JArray)catalog["races"]){
     Check(((string)race["desc"]).Contains("Возраст и жизнь:"),"description available at creation");
     var hero=CharacterCreation.Create(catalog,"Подводный тест",race,cls,bg,stats,new JObject(),"manual");
     Check((string)hero["raceId"]==(string)race["id"],"race ID preserved");
     Check(JToken.DeepEquals(hero["raceFeatureDescriptions"],race["seed"]["raceFeatureDescriptions"]),"full lore and age copied into sheet");
     Check(((JArray)hero["raceFeatureDescriptions"]).Any(x=>x.ToString().Contains("старые")),"age stages reach saved sheet");
     foreach(string stat in new[]{"str","dex","con","int","wis","cha"})Check((int)hero["stats"][stat]==(int)race["seed"]["stats"][stat],"race stat bonus applied exactly once");
     Check((string)hero["speed"]==(string)race["seed"]["speed"],"walking/swimming speed preserved");
     Check((string)hero["size"]==(string)race["seed"]["size"],"size preserved");
     Check(JToken.DeepEquals(hero["raceMechanics"],race["seed"]["raceMechanics"]),"mechanics preserved");
     Check(((JArray)hero["contentPackages"]).Any(p=>(string)p["id"]==(string)race["packageId"]),"package provenance recorded");
     string path=Path.Combine(tmp,(string)race["id"]+".json");CharacterSheetStore.Save(path,new LegacyCharacterArchive(hero.ToString()));
     Check(JToken.DeepEquals(CharacterSheetStore.Load(path).Snapshot(0),hero),"actual sheet save/reload roundtrip");
     if((string)race["id"]=="merrow")Check((string)hero["size"]=="Большой"&&!(bool)hero["raceMechanics"]["amphibious"],"large merrow cannot breathe air by flag");
     if(new[]{"sahuagin","locathah"}.Contains((string)race["id"]))Check(!(bool)hero["raceMechanics"]["amphibious"]&&hero["raceFeatureDescriptions"].ToString().Contains("4 часа"),"limited amphibious races do not get unrestricted flag");
    }
    var triton=(JObject)((JArray)catalog["races"]).Single(x=>(string)x["id"]=="triton");
    foreach(var prop in ((JObject)legacy["races"][0]["seed"]).Properties().Where(p=>p.Name!="raceFeatureDescriptions"))Check(JToken.DeepEquals(triton["seed"][prop.Name],prop.Value),"triton mechanics unchanged: "+prop.Name);
    store.Remove("dnd.collections.aquatic-races");foreach(var id in pids)store.Remove(id);Check(store.Installed().Count==0,"optional uninstall");
    foreach(var id in pids)Install(Find(id));Check(new WorkshopStore(store.Root).Installed().Count==5,"reinstall and restart");
   }finally{Directory.Delete(tmp,true);}
  }
  Console.WriteLine("AQUATIC_RUNTIME_PASS "+checks+" checks: real C# store/install/upgrade/creation/save/restart on both platform selectors; no device GUI claim");
 }
}
