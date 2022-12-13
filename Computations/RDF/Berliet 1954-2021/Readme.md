# Transform Berliet 1954-2021 Building Dataset from GeoJSON (JSON) to GeoJSON (RDF/XML)
An RML-based transformation is used to convert this GeoJSON data to RDF/XML.
The RML mappings were generated and effectuated using [Matey](https://rml.io/yarrrml/matey/#) and [YARRRML](https://rml.io/yarrrml/spec/) (see below).

## Supplementary reading
- [Matey](https://rml.io/yarrrml/tutorial/getting-started/)
- [YARRRML](https://rml.io/yarrrml/spec/)
- [RML](https://rml.io/specs/rml/)
- [JsonPath](https://goessner.net/articles/JsonPath/)

## How to execute the transformation

### Stage 0: Browser or local?
The transformation can be executed using a web browser (currently recommended) or locally using NPM and Java.

If you wish to execute these transformations using a web browser, navigate to the [Matey](https://rml.io/yarrrml/matey/#) website

If you wish to execute them locally follow the instructions in section [Writing rules on your computer](https://rml.io/yarrrml/tutorial/getting-started/#writing-rules-on-your-computer) of the Matey getting started guide.

Note that these instructions will be given assuming a web browser is used.

### Stage 1: Generate RML mappings
1. Copy+paste the contents of the `./yarrrml.yaml` file into the **Input: YARRRML** field of the Matey webpage
   - ![image](https://user-images.githubusercontent.com/23373264/207301313-8e7ac3b5-88e7-4d8c-a1a4-d9cec4d04a47.png)
2. Click on the **Generate RML** action button
   - ![image](https://user-images.githubusercontent.com/23373264/207301355-58fe8289-f594-4a8d-a405-68be1c6aa1c6.png)
* You should see the **Output: RML** field autofill with the corresponding mappings

### Stage 2: Transform dataset
1. Download and unpack the dataset from [Nextcloud](https://partage.liris.cnrs.fr/index.php/s/g3pzCjodEcps2o6)
2. Copy+paste the contents of the first file into the **Input:Data** field of the Matey webpage
   - ![image](https://user-images.githubusercontent.com/23373264/207301170-f742ff45-4931-42f8-ba7c-86f5418eb40a.png)
3. Click on the **Generate LD** action button
   - ![image](https://user-images.githubusercontent.com/23373264/207301424-f74cbcaa-b12b-4393-9913-c8df051159dc.png)
4. Click on the **Output: Turtle/TriG** then from the dropdown menu click **Download** to download the transformed file
   - ![image](https://user-images.githubusercontent.com/23373264/207301709-8c93f45d-dea2-4855-8fef-4a1127eac93e.png)
5. Repeat steps 2-4 for each file in the dataset

## Notes
RML will ignore `null` JSON fields. For most GeoJSON properties, this is normally a good thing as it avoids generating unecessary data. However, the proposed transformations use the `$.features.properties.ID` property in order to create a URI for each feature and its geometry. This means that **features with an `ID` property of `null` will be ignored by the RML**.
