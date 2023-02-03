# CrossPlatform2023

## Dataset Introduction
Recently, a growing body of research has realized that live chat via modern communication platforms plays an increasingly important role in OSS (Open Source Software) collaborative development. Among these platforms, Gitter has emerged as a popular choice since it is directed toward GitHub projects by account sharing and activity subscribing. But little is known about how could Gitter affect the OSS development on GitHub. Who are the developers being active in both social and technical platforms, and how important are they?

To bridge the gap, we perform an in-depth cross-platform analysis on Gitter and GitHub. Seven popular open source communities that both use Gitter and GitHub platforms are selected as our studied subjects, which leads to 1,546,127 utterances from 37,060 chatting developers on Gitter and 395,664 development activities contributed by 89,858 developers on GitHub, with cross-links between developer accounts on both platforms, referred as cross-platform developers (CPDs). 


## Dataset Strcture
### data/
- `data/COMMUNITY_NAME/` contains Gitter chat log file, GitHub activity files and CPD list of this community.
    - `COMMUNITY_Gitter.txt`: Gitter chat log file
    - `COMMUNITY_commits.json`: GitHub commit record
    - `COMMUNITY_issues.json`: GitHub issue record
    - `COMMUNITY_prs.json`: GitHub pull request record
    - `cross_platform_devs.txt`: list of CPDs' usernames


### images/
- `images/` contains the network visualization of Gitter and GitHub collaboration structure of the seven selected communities. Red node denotes CPD, and yellow for non-CPDs. The size of each node is associated with the SLC value of the developer. 
    - `COMMUNITY_gitter.png`: Gitter network
    - `COMMUNITY_github.png`: GitHub network
- Based on the observation of the seven networks, we find that:
    - In the social networks of Deeplearning4j, Angular, and Typescript, CPDs are focal points on both the Gitter network and the GitHub network. 
    - While in the social networks of Appium, Docker, Nodejs, and Ethereum, CPDs are focal points on the Gitter network but are non-focal points on the GitHub network.
