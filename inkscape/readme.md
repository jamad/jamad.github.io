### reference
* http://tavmjong.free.fr/INKSCAPE/MANUAL/html/
* https://inkscape.paix.jp/sitemap/

### decision make for 0.01mm grid
* SVG definition : 1 px = 1/96 inch ( i.e. 1 px = 25.4 mm / 96 ≒ 0.2645 mm )
* inkscape internal xml precision :  1/1000 px  (i.e. 0.0002646 mm )
* but lasercut usually ignore 0.01 mm
* I decided to use 0.01mm grid for my work based on my output card result
* <img height="200" alt="image" src="https://github.com/user-attachments/assets/fc87165f-be72-4c81-b065-74e3b2316c03" /> actually, inkscape cannot zoom in after this level



### the version I use 
<img width="748" height="151" alt="{2095F0BA-9981-461C-AC30-86943F5A05CE}" src="https://github.com/user-attachments/assets/7e7b3dab-2a30-4f46-94c0-2e97e48206ad" />

### important initial settings
* better to change for snapping for lasercut data
<img width="400" height="190" alt="{58B9EC1B-AF08-40C2-8431-782443B84357}" src="https://github.com/user-attachments/assets/02fa532d-d312-48e5-b8a8-10cc4fedd4be" />

* unexpected then expected
<img width="340" height="111" alt="{334A672F-61C1-43C0-84F8-C290F42CFD38}" src="https://github.com/user-attachments/assets/e57a2345-714a-48f8-9a7b-29339b016337" /> 
<img width="379" height="140" alt="{8074D7DB-5E3D-4F54-83C8-75A7ACED62F7}" src="https://github.com/user-attachments/assets/ca282a8f-309c-442b-ad31-4cb0fff4f22f" />

---

### troubleshooting 
# Issue 1
## Problem : How to remove double line?
  * An example : 2 rectangles touch like the following have 1 duplicated line

  <img width="389" height="178" alt="{EEE45871-41E9-4DBF-B904-93528AA35B40}" src="https://github.com/user-attachments/assets/b282e331-b131-406d-b489-e6d6531020d3" />

## Solution 1: use extensions > cutlings > remove duplicate lines  [inkscape-extension-removeduplicatelines](https://cutlings.datafil.no/inkscape-extension-removeduplicatelines) 
  1. First off, convert object to path for the following operation ( ctrl+K to merge data could be safer )

  <img width="286" height="60" alt="{0BB483F6-32D3-440F-BEDD-FEF172DA4D61}" src="https://github.com/user-attachments/assets/f5dc0824-3908-47f4-ae89-062dc4349c3e" />

  2. use remove duplicate lines ( `%AppData%\inkscape\extensions` should have the extension)　with 0.1 ( 0.0 might not merge )
  <img height="92" alt="{C8CA67B5-5CFD-42EA-AEF8-F29FF4B28806}" src="https://github.com/user-attachments/assets/46070d7d-22f0-4558-bb59-055d29a05502" />
  <img height="191" alt="{48F84F07-FA18-469F-A087-79C8DF20B1F4}" src="https://github.com/user-attachments/assets/d6e31a35-9d00-4b6c-a7be-389372d28b52" />
  <img height="240" alt="{B2F20569-3A82-4D8A-8BFD-28FFE577DDC6}" src="https://github.com/user-attachments/assets/6de9a78f-5fa2-4e64-896d-f656516e1b89" />

  3. see data change
  
  <img height="240" alt="{DD7948C8-DC85-4E4F-95F1-6855AA5D3F66}" src="https://github.com/user-attachments/assets/f7c20f23-0088-4863-887c-444b48554266" />

  * Note 1: actually, duplicated lines looks thicker than single lines
  
  <img height="240" alt="{CA0EC30E-6FE3-46E1-9017-CC503E3B8324}" src="https://github.com/user-attachments/assets/37cee28c-eab6-4e2c-9626-e68b437a4466" />

  * Note 2: too many lines seems to fails , so try smaller number of lines again
  
  <img height="240" alt="{4FBFA365-7161-4279-9ABC-D54F89BCF5EF}" src="https://github.com/user-attachments/assets/fc2e8d55-0351-4510-948c-697976b5d826" />

  * The case with all single lines
  <img height="240" alt="{E628067A-178C-4DAB-B718-D473B9AA91FD}" src="https://github.com/user-attachments/assets/39f8074c-dde2-4c9e-81a1-de06c078bf54" />

---

  <img height="160" alt="{E31B1D59-76A0-40A2-ADBF-95B8DCC10348}" src="https://github.com/user-attachments/assets/e09a5bf6-030f-43ff-826a-0846a8c5ddff" /> 
  <img height="160" alt="{9F67C7F1-2B3E-4610-BCAF-0A7C03DFC4DD}" src="https://github.com/user-attachments/assets/9862b48e-0d72-4abc-85ec-5e8182f52f54" /> 
  <img height="160" alt="{F49ADB42-37F1-4BE4-BFE9-6B8A79CFE9E4}" src="https://github.com/user-attachments/assets/add25342-92ea-4b42-bc4e-1c2f8d9054e0" />

# issue 2
## problem : how to merge the same position nodes? 
<img height="240" alt="{ADED5F06-B80E-434D-88C8-854C1604F183}" src="https://github.com/user-attachments/assets/bf1a3d51-0a8f-4b63-8f8a-bacf3cb044fe" />

## Solution : removeDuplicateNodes.py  [remove-duplicate-nodes/](https://cutlings.datafil.no/remove-duplicate-nodes/)
* note : I am making the simpler version [here](https://gist.github.com/jamad/ec12541c04789172e8f4cac3cd045f0d) 
* first , ctrl+K to merge as single path, then extension `remove duplicated nodes` , thick line preview might be good improvement idea because visual helps the change
<img height="160" alt="{D24465F5-D228-420F-A695-693263B2F5B8}" src="https://github.com/user-attachments/assets/01b87120-fc6d-4a1f-98e2-4e6705f067c3" />
<img height="160" alt="{F4C0D2D5-9CF9-44FC-9886-2D93E01EF3BD}" src="https://github.com/user-attachments/assets/c18b846f-a082-4e5f-8d41-dd7fd233076d" />
<img height="160" alt="{F6719C58-540D-4A12-A503-950AFDD8D915}" src="https://github.com/user-attachments/assets/7847e481-25bd-4c66-83b0-75202fdfb379" />


# issue 3
## problem : how to prevent sketchup pdf has double lines
## Solution : use select same fill by selecting a no fill object. Then move and use the lines that has no duplicates. 
<img height="240" alt="{511EC258-5C9A-457D-A9C7-45035EE7D6EF}" src="https://github.com/user-attachments/assets/3e5d0e42-7b28-425f-ad8b-eaa7bda841c1" />
<img height="240" alt="{EC0CAF33-A9EB-442F-8A79-E1A54DDB764D}" src="https://github.com/user-attachments/assets/18363e35-5f36-443e-a0e5-e58155db6441" />




