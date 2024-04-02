# Bringing Open Source Communication and Development Together: A Cross-Platform Study on Gitter and GitHub 

## 1 Introduction
&ensp;&ensp;Recently, a growing body of research has realized that live chat via modern communication platforms plays an increasingly important role in OSS (Open Source Software) collaborative development. Among these platforms, Gitter has emerged as a popular choice since it is directed toward GitHub projects by account sharing and activity subscribing. But little is known about how could Gitter affect the OSS development on GitHub. Who are the developers being active in both social and technical platforms, and how important are they? To bridge the gap, we perform an in-depth cross-platform analysis on Gitter and GitHub, two representative platforms for live communication and distributed development, to explore the characteristics of cross-platform contributors (CPCs) and whether live chat can provoke open source development. 

## 2 Study Design
### 2.1 Research Questions
- RQ1 (CPCs’ Role and Contribution): Who are the developers being active in both Gitter and GitHub, and how important are they?
- RQ2 (CPCs’ Communication Preference): What topics do CPCs in different roles prefer on Gitter?
- RQ3 (CPCs’ Behavioral Consistency): Do CPCs behave consistently across Gitter and GitHub?
- RQ4 (Gitter’s Impact on OSS Contribution): How does Gitter affect OSS contribution on GitHub?

### 2.2 Dataset
Seven popular open source communities that both use Gitter and GitHub platforms are selected as our studied subjects, which leads to **`1,546,127`** utterances from **`37,060`** chatting developers on Gitter and **`395,664`** development activities contributed by **`89,858`** developers on GitHub, with cross-links between developer accounts on both platforms, referred as cross-platform contributors (CPCs). Detailed statistics are shown in this table:

![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/dataset.png)<br>

### (1) Studied Communities
&ensp;&ensp;We build our cross-platform dataset based on Shi et al.’s Gitter Data<sup>[1]</sup>. We select seven out of eight OSS communities from their dataset by excluding the one that does not host source code on GitHub. The selected communities include: [Angular](https://angular.io/), [Appium](http://appium.io/), [DL4J](https://deeplearning4j.org/), [Docker](https://www.docker.com/), [Ethereum](https://ethereum.org/en/), [Nodejs](https://nodejs.org/en/), and [Typescript](https://www.typescriptlang.org/) from the domains including frontend framework, mobile, data science, DevOps, blockchain platform, web application framework, and programming language, respectively.

### (2) Data Collection
&ensp;&ensp;For Gitter data, we select the Gitter utterances provided by Shi et al.<sup>[1]</sup> and extend it to `"2022-09-25"`, and collect accounts of utterance posters in the chatroom.

&ensp;&ensp;For GitHub data, we leverage [GitHub REST API](https://docs.github.com/en/rest) to obtain activity records including commits, issue reports, and pull requests. Each one of them contains the following information: activity conductor, time, activity description, and the id-number. Commenters' information (commenting time, username) is recorded in issues and pull requests as well. Additionally, pull requests also contain their reviewers and related commits. The GitHub data is as of `"2022-09-25"` as well. When processing the data from GitHub, we first remove automatic bot accounts using the classification model proposed by Golzadeh et al.<sup>[2]</sup> that achieves an F1-score of 0.98, and then resolve aliases using the [method](https://github.com/bvasiles/ght_unmasking_aliases) proposed by Vasilescu et al.<sup>[3]</sup>. 

## 3 Results
### 3.1 RQ1: CPCs' Role and Contribution
![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ1-role.png)<br>

This figure shows the roles of CPCs and their contribution to OSS communication and development. 
- The left pie chart describes the distribution of CPCs’ five roles. We can see that 61.7% CPCs are issue reporters, followed by commenters (24.3%), peripheral developers (9.7%), code reviewers (3.5%), and core developers (0.8%). 
- The donut charts on the right exhibit CPCs’ contributions. We can see that, despite CPCs only accounting for 12.2% of the Gitter population, 61% of chat utterances are posted by them. The same phenomenon is observed in the GitHub platform. CPCs take up 5% of the GitHub population, but contribute to 21% commits, 14% issues, 18% reviews, and 18% comments. Even more exaggerated, the core developers in CPCs only account for 0.04% GitHub population, but contribute to 19% commits, as highlighted on the bottom left.

| **Finding 1**: CPCs only take up a small portion of developers on Gitter (12.2%) and GitHub (5.0%), but they contribute to more than 3/5 utterances on Gitter, and nearly 1/5 contributions on GitHub. Even more exaggerated, the core developers in CPCs only account for 0.04% GitHub population, but contribute to 19% commits. |
| :-----|

![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ1-both_focal.png)<br>
![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ1-focal_only_in_Gitter.png)<br>

Furthermore, to show their importance in coordinating communication and development, we visualize CPCs’ SLC scores based on the Gitter and GitHub social networks. Red node denotes CPC, and yellow for non-CPCs. The size of each node is associated with the SLC value of the developer. Based on the observation of the fourteen networks, we find that:
- In the social networks of **Deeplearning4j**, **Angular**, and **Typescript**, CPCs are focal points on both the Gitter network and the GitHub network. 
- While in the social networks of **Appium**, **Docker**, **Nodejs**, and **Ethereum**, CPCs are focal points on the Gitter network but are non-focal points on the GitHub network.

| **Finding 2**: Among all the seven OSS communities, CPCs always coordinate OSS communications by playing as focal points on the Gitter platforms.|
| :-----|

### 3.2 RQ2: CPCs' Communication Preference
![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ2-topic.png)<br>
This table illustrates the dialog topic distribution for different roles of CPCs. We can see that *core developers* prefer to participate in dialogs discussing "Design". *Peripheral developers* are more likely to participate in social chatting and discuss unwanted behaviors and errors. *Issue reporters* are nearly the largest population that participates in all the topics, and their percentages range from 29.6% to 66.7%. Among all the dialogs, they discuss API changes most. The *reviewers* are worthy of the name, they also prefer to participate in conversations about code review and reliability issues on Gitter. They showed little preference for “API change,” “Unwanted behavior,” and
“Design.” The *commenters* are not interested in API change (6.1%), however, they showed similar interest in other topics, ranging from 15.4% to 22.8%.

| **Finding 3**: On the Gitter platform, core OSS developers are more interested in discussing designs, while peripheral OSS developers are more likely to participate in social chatting, discussing unwanted behaviors and errors.|
| :-----|

### 3.3 RQ3: CPCs' Behavioral Consistency
![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ3-activeness.png)<br>
The left figure shows the correlation analysis result of Gitter and GitHub activeness. There is only a weak and slight correlation between Gitter and GitHub activeness. Some developers cluster near the horizontal and vertical axis instead of the center, indicating their 𝐴𝑐𝑡𝑖𝑣𝑒𝑛𝑒𝑠𝑠_𝐺𝑖𝑡𝑡𝑒𝑟 does not align with 𝐴𝑐𝑡𝑖𝑣𝑒𝑛𝑒𝑠𝑠_𝐺𝑖𝑡𝐻𝑢𝑏 all the time. The far-out values that are highly active on one platform while much less active on the other might be because the developers’ effort is limited so they can not afford to be both highly active on Gitter and GitHub. 

The right figure visualizes the change of cumulative activeness correlation throughout time. In all cases, the correlation coefficient r rises to peak during the early stage of Gitter usage. Then r starts to decline until reaching a flattening out, where correlation is weak in the late and stable stage of OSS.  This is probably related to the evolution of the OSS community. When Gitter was first introduced to these projects, the project contributors were actively developing and testing on GitHub and discussing these developmental problems on Gitter, resulting in a relevantly high correlation during this period. However, with the evolution and growth of the OSS communities, more commenters and issue reporters were engaged in Gitter live chat, asking questions such as API usage that are less relevant to GitHub developmental activities and making occasional contributions. Additionally, the active contributor might retire or take breaks from making GitHub contributions but are still active on Gitter.11 These CPCs’ discussions are active on Gitter but their contribution is much less on GitHub, leading to a mismatch and thereby a weakening correlation relationship.

| **Finding 4**: Broadly, there is merely a weak correlation between Gitter activeness and GitHub activeness. However, the cumulative activeness correlation changes over time, following a fast rise and a steady decline trend, until converging on a weak correlation.|
| :-----|

![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ3-sankey.png)<br>
This sankey diagram exhibits the flow of CPCs’ influence on GitHub and Gitter. The length of black lines represents the number of CPCs that fall into the corresponding SLC quarter. The width of the connections is proportional to the number of CPCs who shift from a quarter in one platform to a quarter in the other. We can see that about 70.2% connections are curved, which means most CPCs’ social influence largely migrates between platforms. 

| **Finding 5**: The level of CPCs’ social influence frequently changes between Gitter and GitHub. Despite Some contributors have a low social influence level on GitHub, they can be highly influential on Gitter.|
| :-----|

![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ3-overlap.png)<br>

This table shows the number of identified Gitter communication groups and GitHub collaboration groups, and the average size of the groups. We can see that except for Deeplearning4j, most of the studied OSS communities have zero or small overlaps between their Gitter groups and GitHub groups, indicating CPCs’ collaboration groups on Gitter rarely intersect with their collaboration groups on GitHub. This reveals that the developers who collaborate with each other on GitHub do not frequently communicate on Gitter, and vice versa.

| **Finding 6**: The CPCs’ collaboration groups on Gitter rarely intersect with their collaboration groups on GitHub.|
| :-----|

### 3.4 RQ4: Gitter's Impact on OSS Contribution
#### 3.4.1 Impact on New Contributors
![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ5.png)<br>
Among all the GitHub developers, we find that 2.5% (2,204/89,858) developers have participated in Gitter dialogs before their first contribution to GitHub. Limited by the effort, we randomly sample 200 of the dialogs, carefully read their utterances, and classify them into six categories as shown in this figure.  In terms of motivation, 90.5% new contributors are self-motivated (NC1-4, NC6), and 7% are motivated by core developers. In terms of identity, 59.5% (NC1, NC3, NC6) are OSS product users, and 38% (NC2, NC4-5) are other developers who are interested in the OSS products. Note that, 2.5% are rare cases that are considered as others.

| **Finding 7**: As a recently released communication platform, the amount of new contributors who participated in live chat before first GitHub contribution accounts for 2.5% of the population. 56.7% of them are OSS product users, and 39.6% are other interested developers. Gitter plays a positive role in promoting issue reporting and resolving. Core developers are one of the motivating factors that can attract new contributors via Gitter.|
| :-----|

#### 3.4.2 Impact on Onboarded Contributors
![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ4-contribution.png)<br>

The violin plot in Figure 9(a) compares the CPCs’ GitHub contribution (committing, issue reporting, reviewing, and commenting) with that of other GitHub developers. The inside box plots show the quartiles and median of the distribution, and the horizontal red line denotes the mean value. We can see that the contribution from CPCs outstrips non-CPCs in terms of all four types of development activities. The middle and upper part of the violin of CPCs is wider than non-CPCs, indicating CPCs include more active contributors. A number of non-CPCs cluster at the bottom of the violin makes the upper part less wide, which means there are more one-time contributors in developers who do not chat on Gitter.

However, according to Figure 9(b), only the p-value for PR approval time is less than 0.001, indicating CPC- proposed pull requests take a shorter time to be resolved than those proposed by non-CPCs. While p-values for other activities are all larger than 0.1. From the violin plots, we can see that the data distribution of Response rate, Issue closure rate, PR approval rate and Commit frequency of CPC and non-CPCs is quite similar, while CPC’s Issue resolution time are slightly longer than that of non-CPCs.

| **Finding 8**: The communication on Gitter might have a positive impact on some GitHub onboarded contributions, since GitHub developers who communicate on Gitter have a significantly higher contribution with regard to commit, issue, review, comment and PR approval time than those who do not communicate on Gitter.|
| :-----|

#### 3.4.3 Impact on Returned Code Contributers
![image](https://github.com/CrossPlatform2023/CrossPlatform2023/blob/main/images/RQ4-return.png)<br>

Figure(a) shows two quadrants representing GitHub and Gitter, respectively. The upper quadrant shows the number of developers in the corresponding GitHub states, and the lower quadrant tells us how many of them communicate in the Gitter platform when they are in the corresponding state. In spite of being inactive (BREAK or GONE) on GitHub, about 2.7% of developers participate in live chat in the meantime. This indicates that not making any contribution to the GitHub repository does not mean the contributors leave the communit. They might be active on other platforms that are related to this project, such as communicating on live chat. Inspired by this phenomenon, we further investigate whether developers who communicate on live chat have a higher possibility of return. As shown in Figure(b), G1 (developers who use Gitter) has a higher probability of returning to ACTIVE than G2 (developers who do not use Gitter) by 7.1%, indicating live chat communication has a positive effect on inactive developers’ returning.

| **Finding 9**: The communication on Gitter has a positive impact on GitHub returned contributions. GitHub Developers who communicate on Gitter have a higher probability of returning to contributing than those who do not communicate on Gitter. We observe that there are 2.7% developers who have been inactive on GitHub still participate in discussions on Gitter.|
| :-----|


## 4 Diretory Structure
### data/
- `data/COMMUNITY_NAME/` contains Gitter chat log file, GitHub activity files and CPC list of this community.
    - `COMMUNITY_Gitter.txt`: Gitter chat log file
    - `COMMUNITY_commits.json`: GitHub commit record
    - `COMMUNITY_issues.json`: GitHub issue record
    - `COMMUNITY_prs.json`: GitHub pull request record
    - `cross_platform_devs.txt`: list of CPCs' usernames


### RQ1_networks/
- `RQ1_networks/` contains the network visualization of Gitter and GitHub collaboration structure of the seven selected communities. 
    - `COMMUNITY_gitter.png`: Gitter network
    - `COMMUNITY_github.png`: GitHub network

### images/
- This folder contains images of the dataset and results.

### scripts/
- scripts to collect and process data


## 5 References
[1] Lin Shi, Xiao Chen, Ye Yang, Hanzhi Jiang, Ziyou Jiang, Nan Niu, and Qing Wang. 2021. A First Look at Developers’ Live Chat on Gitter. In Proceedings of the 29th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 391–403. <br>
[2] Mehdi Golzadeh, Alexandre Decan, Damien Legay, and Tom Mens. 2021. A 1230 Ground-truth Dataset and Classification Model for Detecting Bots in GitHub 1231 Issue and PR Comments. Journal of Systems and Software 175 (2021), 110911. <br>
[3] Bogdan Vasilescu, Alexander Serebrenik, and Vladimir Filkov. 2015. A Data Set for Social Diversity Studies of GitHub Teams. In 12th Working Conference on Mining Software Repositories, Data Track (MSR). IEEE, 514–517.
