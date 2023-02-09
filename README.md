# CrossPlatform2023

## 1 Dataset Introduction
&ensp;&ensp;Recently, a growing body of research has realized that live chat via modern communication platforms plays an increasingly important role in OSS (Open Source Software) collaborative development. Among these platforms, Gitter has emerged as a popular choice since it is directed toward GitHub projects by account sharing and activity subscribing. But little is known about how could Gitter affect the OSS development on GitHub. Who are the developers being active in both social and technical platforms, and how important are they?

&ensp;&ensp;To bridge the gap, we perform an in-depth cross-platform analysis on Gitter and GitHub. Seven popular open source communities that both use Gitter and GitHub platforms are selected as our studied subjects, which leads to **`1,546,127`** utterances from **`37,060`** chatting developers on Gitter and **`395,664`** development activities contributed by **`89,858`** developers on GitHub, with cross-links between developer accounts on both platforms, referred as cross-platform developers (CPDs). Detailed statistics are shown in this table:



### 1.1 Studied Communities
&ensp;&ensp;We build our cross-platform dataset based on Shi et al.’s Gitter Data<sup>[1]</sup>. We select seven out of eight OSS communities from their dataset by excluding the one that does not host source code on GitHub. The selected communities include: [Angular](https://angular.io/), [Appium](http://appium.io/), [DL4J](https://deeplearning4j.org/), [Docker](https://www.docker.com/), [Ethereum](https://ethereum.org/en/), [Nodejs](https://nodejs.org/en/), and [Typescript](https://www.typescriptlang.org/) from the domains including frontend framework, mobile, data science, DevOps, blockchain platform, web application framework, and programming language, respectively.

### 1.2 Data Collection
&ensp;&ensp;For Gitter data, we select the Gitter utterances provided by Shi et al.<sup>[1]</sup>, and collect accounts of utterance posters in the chatroom.

&ensp;&ensp;For GitHub data, we leverage [GitHub REST API](https://docs.github.com/en/rest) to obtain activity records including commits, issue reports, and pull requests. Each one of them contains the following information: activity conductor, time, activity description, and the id-number. Commenters' information (commenting time, username) is recorded in issues and pull requests as well. Additionally, pull requests also contain their reviewers and related commits. When processing the data from GitHub, we first remove automatic bot accounts using the classification model proposed by Golzadeh et al.<sup>[2]</sup> that achieves an F1-score of 0.98, and then resolve aliases using the method proposed by Vasilescu et al.<sup>[3]</sup>. 


## 2 Dataset Structure
### data/
- `data/COMMUNITY_NAME/` contains Gitter chat log file, GitHub activity files and CPD list of this community.
    - `COMMUNITY_Gitter.txt`: Gitter chat log file
    - `COMMUNITY_commits.json`: GitHub commit record
    - `COMMUNITY_issues.json`: GitHub issue record
    - `COMMUNITY_prs.json`: GitHub pull request record
    - `cross_platform_devs.txt`: list of CPDs' usernames


### RQ1_networks/
- `RQ1_networks/` contains the network visualization of Gitter and GitHub collaboration structure of the seven selected communities. Red node denotes CPD, and yellow for non-CPDs. The size of each node is associated with the SLC value of the developer. 
    - `COMMUNITY_gitter.png`: Gitter network
    - `COMMUNITY_github.png`: GitHub network
- Based on the observation of the seven networks, we find that:
    - In the social networks of **Deeplearning4j**, **Angular**, and **Typescript**, CPDs are focal points on both the Gitter network and the GitHub network. 
    - While in the social networks of **Appium**, **Docker**, **Nodejs**, and **Ethereum**, CPDs are focal points on the Gitter network but are non-focal points on the GitHub network.




## 3 References
[1] Lin Shi, Xiao Chen, Ye Yang, Hanzhi Jiang, Ziyou Jiang, Nan Niu, and Qing Wang. 2021. A First Look at Developers’ Live Chat on Gitter. In Proceedings of the 29th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 391–403. <br>
[2] Mehdi Golzadeh, Alexandre Decan, Damien Legay, and Tom Mens. 2021. A 1230 Ground-truth Dataset and Classification Model for Detecting Bots in GitHub 1231 Issue and PR Comments. Journal of Systems and Software 175 (2021), 110911. <br>
[3] Bogdan Vasilescu, Alexander Serebrenik, and Vladimir Filkov. 2015. A Data Set for Social Diversity Studies of GitHub Teams. In 12th Working Conference on Mining Software Repositories, Data Track (MSR). IEEE, 514–517.