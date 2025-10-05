### reference
* http://tavmjong.free.fr/INKSCAPE/MANUAL/html/
* https://inkscape.paix.jp/sitemap/

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

## Solution 1: use [inkscape-extension-removeduplicatelines](https://cutlings.datafil.no/inkscape-extension-removeduplicatelines) 
  1. First off, convert object to path for the following operation
  <img width="286" height="60" alt="{0BB483F6-32D3-440F-BEDD-FEF172DA4D61}" src="https://github.com/user-attachments/assets/f5dc0824-3908-47f4-ae89-062dc4349c3e" />

  2. use remove duplicate lines 
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


