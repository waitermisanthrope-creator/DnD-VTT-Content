using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using Newtonsoft.Json.Linq;
using DndVtt.UnityPrototype;

static class RaceDescriptionChecks
{
 static int checks;
 static void Check(bool ok,string name){if(!ok)throw new Exception(name);checks++;}
 public static void Run(string root)
 {
  checks=0;
  var manifests=WorkshopStore.Catalog(File.ReadAllText(Path.Combine(root,"catalog/v3/index.json")),"packages").OfType<JObject>().ToArray();
  var races=manifests.Where(m=>(string)m["type"]=="race").ToArray();
  var full=manifests.Single(m=>(string)m["id"]=="dnd.collections.races");
  string[] water={"dnd.race.triton","dnd.race.kuo_toa","dnd.race.merrow","dnd.race.sahuagin","dnd.race.locathah"};
  string Payload(JObject m)=>Path.Combine(root,"packages",Path.GetFileName((string)m["url"]));
  Check(races.Length==47,"47 existing races");
  foreach(var m in races){var d=WorkshopStore.ValidateData(m,File.ReadAllText(Payload(m)));foreach(JObject race in (JArray)d["races"]){
   string desc=(string)race["desc"]??"";
   Check(desc.Length>350&&!desc.StartsWith("Дополнение:")&&desc.Contains("Возраст и жизнь:"),"Full lore and age missing: "+m["id"]);
  }}
  var cls=(JObject)JObject.Parse(File.ReadAllText(Path.Combine(root,"packages/dnd.class.blood_hunter.json")))["classes"][0];
  var bg=JObject.Parse("{name:'Test background',seed:{},choices:[]}");
  var stats=JObject.Parse("{str:10,dex:10,con:10,int:10,wis:10,cha:10}");
  foreach(string platform in new[]{"android-arm64","windows-x64"}){
   string tmp=Path.Combine(Path.GetTempPath(),"race-lore-"+Guid.NewGuid());Directory.CreateDirectory(tmp);
   try{
    var store=new WorkshopStore(Path.Combine(tmp,"store"));
    void Install(JObject m){string download=Path.Combine(tmp,"download.json");File.Copy(Payload(m),download,true);store.Install(m,download,platform,"6000.3.26f1");}
    JObject OldManifest(JObject m,string file,string version){
     var copy=(JObject)m.DeepClone();byte[] raw=File.ReadAllBytes(Path.Combine(root,"packages",file));
     copy["version"]=version;copy["url"]="https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/packages/"+file;
     copy["bytes"]=raw.Length;copy["sha256"]=Convert.ToHexString(SHA256.HashData(raw)).ToLowerInvariant();return copy;
    }
    foreach(var m in races)Install(water.Contains((string)m["id"])?m:OldManifest(m,(string)m["id"]+".json","1.0.0"));
    Install(OldManifest(full,"dnd.collections.races-1.0.1.json","1.0.1"));
    var before=store.Creation(JObject.Parse("{races:[],classes:[],feats:[],proficiencies:[]}"));
    var oldRace=(JObject)((JArray)before["races"]).Single(r=>(string)r["id"]=="aasimar");
    var oldHero=CharacterCreation.Create(before,"Старый герой",oldRace,cls,bg,stats,new JObject(),"manual");
    string oldPath=Path.Combine(tmp,"existing-hero.json");CharacterSheetStore.Save(oldPath,new LegacyCharacterArchive(oldHero.ToString()));
    var plan=WorkshopStore.InstallPlan(full,manifests,store.Installed().OfType<JObject>(),platform,"6000.3.26f1",10040);
    Check(plan.Count==43,"Upgrade installs only 42 changed races and the collection marker");
    Check(plan.OfType<JObject>().All(m=>!water.Contains((string)m["id"])),"Aquatic races need no redownload");
    Check((string)plan.Last["id"]=="dnd.collections.races","collection installs last");
    foreach(JObject m in plan)Install(m);
    store=new WorkshopStore(store.Root);
    Check(WorkshopStore.InstallPlan(full,manifests,store.Installed().OfType<JObject>(),platform,"6000.3.26f1",10040).Count==0,"Repeated upgrade is a no-op");
    Check(JToken.DeepEquals(CharacterSheetStore.Load(oldPath).Snapshot(0),oldHero),"Updating mods cannot rewrite an existing hero");
    var catalog=store.Creation(JObject.Parse("{races:[],classes:[],feats:[],proficiencies:[]}"));
    Check(((JArray)catalog["races"]).Count==47,"47 unique race IDs after upgrade and restart");
    catalog["proficiencies"]=new JArray(((JArray)catalog["races"]).OfType<JObject>().SelectMany(r=>((JArray)r["choices"]).OfType<JObject>()).Where(c=>(string)c["id"]=="race_languages").SelectMany(c=>((JArray)c["options"]).OfType<JObject>()).GroupBy(o=>(string)o["id"]).Select(g=>g.First().DeepClone()));
    foreach(JObject race in (JArray)catalog["races"]){
     var answers=new JObject();
     foreach(JObject choice in (JArray)race["choices"]){
      var options=(JArray)choice["options"];int count=(int?)choice["count"]??1;
      var selected=options.Take(count).Select(o=>(o is JObject obj?obj["id"]??obj["name"]:o).DeepClone()).ToArray();
      answers[(string)choice["key"]]=(string)choice["type"]=="multi"?new JArray(selected):selected[0];
     }
     var hero=CharacterCreation.Create(catalog,"Описание — "+race["name"],race,cls,bg,stats,answers,"manual");
     var lore=(JArray)hero["raceFeatureDescriptions"];
     Check(lore!=null&&lore.Any(s=>s.ToString().Contains("Возраст и жизнь:")),"Age survives creation: "+race["id"]);
     Check(JToken.DeepEquals(lore,race["seed"]["raceFeatureDescriptions"]),"Full lore copied into sheet: "+race["id"]);
     Check((string)hero["raceId"]==(string)race["id"],"Stable race ID");
     foreach(string stat in CharacterSheetRules.Stats)Check((int)hero["stats"][stat]==(int?)race["seed"]?["stats"]?[stat] || race["seed"]?["stats"]?[stat]==null&&(int)hero["stats"][stat]==10,"Stats preserved: "+race["id"]+"/"+stat);
     Check(JToken.DeepEquals(hero["choiceState"],answers),"Existing choices preserved");
     string path=Path.Combine(tmp,(string)race["id"]+".json");CharacterSheetStore.Save(path,new LegacyCharacterArchive(hero.ToString()));
     Check(JToken.DeepEquals(CharacterSheetStore.Load(path).Snapshot(0),hero),"Description and mechanics survive save/reload");
     Check(((JArray)hero["contentPackages"]).Any(p=>(string)p["id"]==(string)race["packageId"]&&(string)p["version"]==(string)race["packageVersion"]),"Package version tracked");
    }
   }finally{Directory.Delete(tmp,true);}
  }
  Console.WriteLine("RACE_DESCRIPTIONS_RUNTIME_PASS "+checks+" checks: all47 races, 42 upgrades, real C# creation/save/restart; Android/Windows selectors, no GUI claim");
 }
}
