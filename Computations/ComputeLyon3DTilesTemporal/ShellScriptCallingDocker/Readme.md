
## Running things
```
mkdir some_output_dir     # e.g.
./DockerComputeLyonCityEvolution.sh some_output_dir
```
The resulting tile set will be located in the `some_output_dir/Result` subdirectory.

## Improving things
 * Automatize the configuration of the IP number that is hardwired in many configuration files. Note that the command `hostname -I` is not even portable. Maybe we should go for docker in docker and dockerise the main shell script ? Will that _really_ slow things down ?
 * At the beginning of the pipeline Bron and Villeurbanne are dealt with. But
   at some point they vanish from the workflow. Fix that !
