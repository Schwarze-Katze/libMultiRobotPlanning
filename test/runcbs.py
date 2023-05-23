import unittest
import subprocess
import yaml
import os
import re

def runCBS(inputFile, createVideo=False, timeout=None, additionalArgs=[]):
  subprocess.run(
    ["./build/cbs",
      "-i", inputFile,
      "-o", "output.yaml"] + additionalArgs,
      check=True,
      timeout=timeout)
  if createVideo:
    subprocess.run(
      ["python3", "../example/visualize.py",
        inputFile,
        "output.yaml",
        "--video", os.path.splitext(os.path.basename(inputFile))[0] + "_cbs.mp4"],
      check=True)
  with open("output.yaml") as output_file:
    return yaml.safe_load(output_file)

def catAgentsPath(dic: dict, Paths: dict):
  scheduleTmp = dic['schedule']
  for key, value in scheduleTmp.items():
      if not key in Paths:
          Paths[key] = []
      Paths[key].extend(value)

if __name__ == '__main__':
  curPath = os.path.dirname(os.path.realpath(__file__))
  outputPath = os.path.join(curPath, "Test-2023.5.23_23.21.23")  # src/output/result_60*40
  yamlPaths = sorted(os.listdir(outputPath),key=lambda s: [int(s) if s.isdigit() else s for s in sum(re.findall(r'(\D+)(\d+)', 'a'+s+'0'), ())])
  Paths = {}
  for yamlPath in yamlPaths:  # src/output/result_60*40/result1/1.yaml
      config=runCBS(outputPath+'/'+yamlPath)
      catAgentsPath(config,Paths)
  scheduleOutput={'schedule':Paths}
  outTmp=yaml.safe_dump(scheduleOutput)
  with open(outputPath+'/catOut.yaml', 'w', encoding='utf-8')as f:
      f.write(outTmp)

