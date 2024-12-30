# AntiCP3 : Prediction of Anticancer Proteins

**AntiCP3** is a tool developed for the prediction of anticancer proteins. This repository contains the standalone code for AntiCP3. In addition to the standalone, AntiCP3 is also available as a pip installable package and can also be accessed through the webserver: [https://webs.iiitd.edu.in/raghava/anticp3/](https://webs.iiitd.edu.in/raghava/anticp3/).

For prediction of anticancer peptides (length less than 50) use [https://webs.iiitd.edu.in/raghava/anticp2/](AntiCP2).

## Installation (For Linux Users)

### Git Clone
- Step: 1
  Users can clone this repository using

  `git clone https://github.com/amisha1699/anticp3.git`

- Step: 2
  Navigate to the directory

  `cd anticp3`

- Step: 3 - Use `environment.yml` (Recommended)

  Run `conda env create -f environment.yml`

- Step: 4
  
  Activate the environment
  `conda activate anticp3` 

- Alternative to Step: 3 - Using `requirements.txt`

  Run `pip install -r requirements.txt`

### Usage

`anticp3.py [-h] [-i INPUT] [-o OUTPUT] [-m {1,2}] [-t THRESHOLD] [-wd WORKING_DIRECTORY]`

Please provide following arguments for successful run

## Example Run:
`anticp3.py -i ./example/example_input.fasta -m 2 -t 0.45 -o example_output.csv -wd ./example/`

| Argument                     | Description                                                                                               | Default Value               |
|------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------|
| `-h, --help`                 | Displays help information.                                                                               | N/A                         |
| `-i INPUT, --input INPUT`    | Input protein sequence(s) in FASTA format.                                                              | Required                    |
| `-o OUTPUT, --output OUTPUT` | Output file for saving results in CSV format.                                                           | `out.csv`                   |
| `-m {1,2}, --model {1,2}`    | Model type: <br>1: AAC + PSSM based ET<br>2: AAC + PSSM + BLAST ensemble (Best Model).                  | `2`                         |
| `-t THRESHOLD`               | Threshold value between 0 and 1.                                                                        | `0.5`                       |
| `-wd WORKING_DIRECTORY`      | Directory path where input/output files are located.                                                    | Current directory of script |

## PIP Installation
`pip3 install anticp3`
