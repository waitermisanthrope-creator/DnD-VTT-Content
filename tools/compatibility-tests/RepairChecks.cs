using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;
using DndVtt.UnityPrototype;
static class RepairChecks
{
 public static void Run(string source)
 {
  int checks=0;
  void Check(bool ok,string name){if(!ok)throw new Exception(name);checks++;}
  void Reject(Action action,string name){bool rejected=false;try{action();}catch(FormatException){rejected=true;}Check(rejected,name);}
  var catalog=WorkshopStore.Catalog(File.ReadAllText(Path.Combine(source,"catalog/v3/index.json")),"packages");
  var manifests=catalog.OfType<JObject>().Where(m=>(string)m["professionalRepairRevision"]=="1.0.0").ToArray();
  var definitions=new Dictionary<string,(JObject item,JObject manifest)>();
  foreach(JObject m in catalog) {
   var p=JObject.Parse(File.ReadAllText(Path.Combine(source,"packages",Path.GetFileName((string)m["url"]))));
   foreach(JObject i in p["items"] as JArray ?? new JArray())definitions.Add((string)i["id"],(i,m));
  }
  Check(manifests.Length==37,"37 optional packages");
  string root=Path.Combine(Path.GetTempPath(),"repair-content-"+Guid.NewGuid());Directory.CreateDirectory(root);
  try {
   void Install(WorkshopStore store,JObject m,string platform){string download=Path.Combine(root,"download.json");File.Copy(Path.Combine(source,"packages",Path.GetFileName((string)m["url"])),download,true);store.Install(m,download,platform,"6000.3.26f1");}
   var combined=new WorkshopStore(Path.Combine(root,"combined"));
   Check(combined.Installed().Count==0,"no automatic packages");
   foreach(var m in manifests) {
    Check(((JArray)m["dependencies"]).Count==0,"damaged loot can be installed independently");
    foreach(var platform in new[]{"android-arm64","windows-x64"}) {
     var store=new WorkshopStore(Path.Combine(root,(string)m["id"]+platform));Install(store,m,platform);
     var restarted=new WorkshopStore(store.Root);Check(restarted.Find((string)m["id"])!=null,"install/restart "+platform);
     Check(restarted.Installed().Count==1,"only chosen package");
     Check(((JArray)restarted.Commerce()["items"]).Count<=100,"published cap respected");
     store.Remove((string)m["id"]);Check(store.Installed().Count==0,"independent uninstall");
    }
    Install(combined,m,"android-arm64");
   }
   var items=((JArray)combined.Commerce()["items"]).OfType<JObject>().ToArray();
   var tools=items.Where(i=>i["professionalTool"]!=null).ToArray();var broken=items.Where(i=>i["brokenVariantOf"]!=null).ToArray();
   Check(tools.Length==56&&broken.Length==2798,"exact professional/repair expansion counts");
   foreach(var item in broken) {
    Check((string)item["inventoryCategory"]=="junk"&&item["effects"]==null&&item["damage"]==null&&item["acBase"]==null&&item["alchemyId"]==null,"broken variants have no equip/consumption/ingredient payload");
    var link=(JObject)item["repairProfile"]["target"];var target=definitions[(string)link["itemId"]];
    Check((string)target.manifest["id"]==(string)link["packageId"]&&(string)target.manifest["version"]==(string)link["packageVersion"]&&(string)target.manifest["sha256"]==(string)link["packageSha256"]&&(string)target.manifest["url"]==(string)link["packageUrl"],"repair reference resolves exact current definition");
    Check((string)item["brokenVariantOf"]==(string)target.item["id"]&&target.item["brokenVariantOf"]==null&&JToken.DeepEquals(item["weight"],target.item["weight"]),"one-way target and all-pieces weight retained");
    Check((bool)item["repairProfile"]["mending"]["requiresAllOriginalPieces"]&&!(bool)item["repairProfile"]["mending"]["restoresMagic"]&&!(bool)item["repairProfile"]["mending"]["restoresCharges"]&&(int)item["repairProfile"]["mending"]["maxBreakDimensionFt"]==1,"mending conditions recorded without magical replenishment");
   }
   Check(Array.IndexOf(CharacterSheetRules.InventoryCategories,"junk")>=2,"broken category has no equip button in published inventory");
   var hammer=tools.Single(i=>(string)i["name"]=="Кузнечный молот");
   Check((string)hammer["professionalTool"]["associatedProficiencyId"]=="p_tool_smith"&&!(bool)hammer["professionalTool"]["grantsProficiency"],"smith hammer has explicit professional role, no proficiency grant");
   var flesh=tools.Single(i=>(string)i["name"]=="Нож для мездрения шкур");Check((string)flesh["professionalTool"]["role"]=="fleshing_knife","explicit fleshing operation");
   var stone=tools.Single(i=>(string)i["name"]=="Точильный камень");Check((string)stone["professionalTool"]["role"]=="whetstone","explicit sharpening tool");
   var vessel=tools.Single(i=>(string)i["name"]=="Пустой алхимический сосуд");Check(((JArray)vessel["containerSpec"]["initialContents"]).Count==0&&(int)vessel["containerSpec"]["capacityMl"]==250&&vessel["effects"]==null,"empty vessel never creates contents or potion effects");
   var hero=JObject.Parse("{id:'repair',name:'Crafter',unknown:{keep:true}}");
   var damaged=broken.Single(i=>(string)i["brokenVariantOf"]==(string)hammer["id"]);
   CommerceRules.AddItem(hero,hammer);CommerceRules.AddItem(hero,damaged,2);
   var owned=(JArray)hero["inventory"]["junk"];Check(owned.Count==2&&(int)owned[0]["count"]==1&&(int)owned[1]["count"]==2,"healthy and broken stocks never merge");
   string before=hero.ToString();Reject(()=>CommerceRules.UseProduct(hero,(JObject)owned[1]),"damaged tool cannot be consumed as product");Check(hero.ToString()==before,"rejected use does not change stock");
   owned[1]["remainingCharges"]=0;owned[1]["magicState"]="lost";owned[1]["provenance"]=JObject.Parse("{owner:'Crafter',source:'found'}");
   Check(JToken.DeepEquals(new LegacyCharacterArchive(new LegacyCharacterArchive(hero.ToString()).Export()).Snapshot(0),hero),"repair links, provenance and depleted/lost state survive save");
   before=hero.ToString();combined.Remove((string)hammer["packageId"]);Check(before==hero.ToString(),"uninstall does not fix/delete owned tools");
   Check((bool)hero["unknown"]["keep"],"unknown character fields preserved");
  }finally{Directory.Delete(root,true);}
  Console.WriteLine("REPAIR_CONTENT_COMPATIBILITY_PASS "+checks+" checks; existing pure runtime only; automatic repair not claimed");
 }
}
