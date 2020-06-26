This directory holds different ways of computing a 3D Tiles tileset with the
[temporal extension](https://doi.org/10.5281/zenodo.3596881) representing the
city of Lyon from 2009 to 2015. The full pipeline of this computation is
described by the following UML activity diagram:

![Tiler Activity Diagram](./Images/TilerActivityDiagramWithoutRendering.png)

The following four ways of automating this computation has been explored:
Note that the most complete one and the only one that is still maintained (i.e.
**you must use this one**) is *ShellScriptCallingDocker*.
  -	[ShellScript](ShellScript/README.md): This version requires that you install
   all the dependencies on your host (which might prove to be quite tricky)...
  - [ShellScriptCallingDocker](ShellScriptCallingDocker): the main control loop
  (i.e. the workflow) of this version is shell-script based but the atomic
  treatments trigger docker containers. They are thus no dependencies to install
  but Docker.
  - [Cwl](Cwl/Readme.md): this version follows the same logic as the
  ShellScriptCallingDocker one, except that the workflow is decribed with
  the [Common Workflow Language (CWL)](https://www.commonwl.org/)
  - [AirFlow](AirFlow/Readme.md): this version uses
  [Airflow](https://airflow.apache.org/) in order to express the workflow.
  Getting this version to run will require you to install many of its heavy duty
  production server dependencies like Kuberntes, a webs-based GUI controler,
  a scheduler, a PostgreSQL database...

Note: the [Docker](Docker/Readme.md) directory holds the docker contexts
required to build the containers which usage is shared by
ShellScriptCallingDocker, Cwl as well as the Airflow versions.

Other pipelining tools in Python:
 - [Prefect Core](https://www.prefect.io/products/core/)
 - [Luigi](https://luigi.readthedocs.io/en/latest/)
 - [d6tflow](https://github.com/d6t/d6tflow)
