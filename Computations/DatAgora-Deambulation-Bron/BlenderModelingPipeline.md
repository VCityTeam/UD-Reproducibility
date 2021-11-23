# Convertion between CityGML and OBJ
The convertion between CityGML and OBJ (Wavefront) files is done with the tool `GMLtoOBJ` (see repo [`Da-POM-Ville-Unity`](https://github.com/VCityTeam/UD-Demo-DatAgora-Deambulation-Bron)).
```
DA-POM-VilleUnity/CityGMLTool BRON_BATI_2018.gml --obj BRON_BATI_2018.obj
```
Warning ! The vanilla code of the `GMLtoOBJ` tool applies an offset (-1800000, -5100000) and then swaps axes ((x, y, z) becomes (y, z, x)). See the following lines in the code:
- https://github.com/VCityTeam/DA-POM-VilleUnity/blob/a6a2295ecb8b827bcbd7799d97703ffa989e58b7/src/Modules/GMLtoOBJ/DataProfile.cpp#L68
- https://github.com/VCityTeam/DA-POM-VilleUnity/blob/a6a2295ecb8b827bcbd7799d97703ffa989e58b7/src/Modules/GMLtoOBJ/main.cpp#L49
- https://github.com/VCityTeam/DA-POM-VilleUnity/blob/a6a2295ecb8b827bcbd7799d97703ffa989e58b7/src/Modules/GMLtoOBJ/GMLtoOBJ.cpp#L149

# Import of OBJ for detailed modeling inside Blender
First, the OBJ file is imported inside Blender : `File->Import->Wavefront (.obj)`.
With coordinates in millions in x and y, it can be hard to *find* the model in the Blender scene.
One way to do so is to go upside view (type `7` on the numeric pad, or click the Z blue disk at the extremity of the Z axis) and extend the view to all scene objects (`SHIFT+C`).
Then, in order to work properly and not to suffer flickering of the model because of high value coordinates, the model is offset again to put the origin somewhere in the domain of the model itself.
To move the center of the model to the origin, select the imported model, then in the top left menu `Object->Set Origin->Origin to Center of Mass (Volume)`, then `SHIFT+S->Selection to Cursor`.
The two resulting offsets applied for the specific case of the detailed model of Bron campus are (5100000, -1800000, 0) and (70874.5625, -49223.44, 194.8617).

# Exporting the model for importation inside UD-Viz
The first step to export the detailed model is to reverse the offsets.
Directly in Blender, this can be done by typing `G, <translation in X>, Tab, <translation in Y>, Tab, <translation in Z>, Enter`.
So apply the reverse offsets (70874.5625, -49223.44, 194.8617) and (5100000, -1800000, 0).

Then, there are two possibilities : exporting to OBJ (which will be converted to 3DTiles) or exporting to GLB (which is imported directly as an asset/GameObject in UD-Viz).

## OBJ and 3DTiles
This way is currently placing correctly the geometry of the model but **the textures are lost in the process** because of the OBJ py3dtiler.
In Blender, `File->Export->Wavefront (.obj)`, then in the `Transform` panel of the newly opened window, be sure to select `-X Forward` and `Z Up` before clicking `Export OBJ`.
Then, the convertion from the OBJ file to a 3DTile is done by the [`ObjTiler`](https://github.com/VCityTeam/py3dtilers/blob/master/py3dtilers/ObjTiler) tool of the [`py3dtilers`](https://github.com/VCityTeam/py3dtilers) repo : `obj-tiler --paths <obj_repository_path>`.
If all went well, the resulting 3DTile can be found in the `obj_tilesets` subdirectory of `py3dtilers` and can be added to the `3DTilesLayers` of UD-Viz.

## GLB
This way is currently supporting the textures of the model, **but the placement of the geometry is wrong**.
In Blender, `File->Export->glTF 2.0 (.glb/.gltf)` then in the `Transform` panel of the newly opened window, be sure to let `+Y Up` checked before clicking on `Export glTF 2.0` as it is assures the canonical transformation between the Blender and the gltf 2.0 referentials is applied.
The resulting GLB file can then be described as a UD-Viz asset and loaded as a `GameObject`.
