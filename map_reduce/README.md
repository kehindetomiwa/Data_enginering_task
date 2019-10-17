# MapReduce 

# code:   
    mapper.py 
    reducer.py
The results of the code was validated with a subset of the dataset in 
biographies.list (see small.list)

you can produce small set with diffent bash commands. But I used:
$ head -100 biographies.list $> small.list 

To run run the code on local machine
do:
```bash
$ cat small.list | python mapper.py  | sort -k1 | python reducer.py &> result.txt 
```



## Running the code over Hadoop clutter with a map-reduce job.
The Hadoop streamer provides the API that allow us write map and reduce task in different programming language.

One your Hadoop NameNode. 
Step one: Identify the location of the Hadoop streamer jar file
``` bash
$ locate hadoop-streaming.jar
```
step 2. set the following variable 
``` bash
$ HADOOP_STREAMING_JAR="/path/to/hadoop-streaming.jar"
```
step 3. Do
``` bash
$ yarn jar $HADOOP_STREAMING_JAR \
-files mapper.py, reducer.sh  -mapper 'python mapper.py' \ -reducer './reducer.sh'   -numReduceTasks 1 \
-input  biographies.list -output word_count_biographies
```
The above command should produce the output of the Reduce task in HDFS in directiry word_count_biographies.

you can check this output with 
``` bash
hdfs dfs -text word_count_biographies/*
```
Note. 
word_count_biographies directory has to be removed or renamed before any subsequent execution of the command in step 3. 
