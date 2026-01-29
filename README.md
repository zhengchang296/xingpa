该替换方式可跳过一帧一帧地更换图片及其图片对齐，同时可以自由的调整帧数。需要准备AssetStudio、UABEA，然后编辑json代码我用的是Visual Studio Code。AssetStudio主要用于查找目标bundle，UABEA主要用于修改bundle。对于部分脚本的使用会在最后讲解。


这里介绍使用同个游戏的其他动画替换原动画的方式，自制动画的方式在整理完会导入到其他分支的readme。


首先，被替换的动画我称作原动画，你自己准备的动画我称作新动画。我这里有两种修改方式。分为同个游戏的其他动画替换原动画和自制动画。


用UABEA解包你新动画对应的bundle文件，将所有所有walk带数字的文件即Sprite文件export dump为json，texture2D文件的图片也要导出；原动画则需要导出assetbundle、animationclip、MONObehaviour的json文件。

<img width="1396" height="864" alt="image" src="https://github.com/user-attachments/assets/9a8f22ba-d854-4181-8570-43b6e841299a" />
<img width="1377" height="888" alt="image" src="https://github.com/user-attachments/assets/1c490d56-62cc-41fe-af84-066044ae4160" />

随后用右侧的插件修改原动画的Texture2D图片，Load导入新动画动画的精灵图即texture2D的图片。

<img width="755" height="614" alt="image" src="https://github.com/user-attachments/assets/0d037de4-2e94-481b-b533-9b401fcec8cd" />

最后，最痛苦的来了。修改新动画每个sprite文件的json文件，在里面找到pathID，替换为原动画动画bundle文件中Texture2D文件的pathID即路径ID。

这步已被相对简化，对应PathID的修改可使用提供的脚本修改。

<img width="629" height="392" alt="image" src="https://github.com/user-attachments/assets/1336fc8d-2328-4ed4-a75c-75e832684eac" />
<img width="293" height="855" alt="image" src="https://github.com/user-attachments/assets/3a9ddd22-bceb-42ac-aa1e-736367d256c4" />

接着将新动画每个sprite的json，import dump对应的原动画Sprite。如果你新动画的帧数小于原动画，记得按顺序将对应的Sprite导入，后直接删除多余的sprite文件即可，记得删数字最大的，。如果新动画帧数大于原动画，那么有两种方法。一定要看完，帧数少和方法二后面还有步骤。

方法一，则需要修改你新动画相应json文件中的m_name。
这一步的对应关系比较复杂，就是你现选取你需要的帧数，如你想导入新动画的00000--00010、00021--00028这些帧，那就修改新动画的名称中带相应数字的json文件，使得里面的m_name变成连续的，即将00021--00028中n_name的数字改为00011--00018，所有文件的n_name必须保持连续，这样动画运行过程中才能在相应的帧数中读取。方法一到这里就结束了，帧数少的和方法二还要往后看。

<img width="431" height="280" alt="image" src="https://github.com/user-attachments/assets/abbe562e-837a-4749-ba17-72a54b15541b" />

方法二，则是让你在原动画bundle中添加Sprite项。我比较推荐这一种。

首先，获得原动画的Sprite的container码，我一般是进到原动画的assetbundle里获得这个的。

<img width="282" height="557" alt="image" src="https://github.com/user-attachments/assets/43b16734-4223-40b2-b757-50641fbd2c62" />
<img width="580" height="298" alt="image" src="https://github.com/user-attachments/assets/6073493f-ff86-4de4-abb2-776a775e221d" />


复制后使用自动PathID脚本，输入first值后得到一个PathID和两类代码。

<img width="1290" height="877" alt="image" src="https://github.com/user-attachments/assets/4cccbbcb-97d8-44f1-bb74-f873ccb3dce7" />

接着，便开始添加Sprite项。使用UABEA左上角file的add，输入PathID，type栏输入Sprite或213都可以，MONO栏不变。

划重点，那个fill Asset with 00s一定不能勾选，如果加入的Sprite勾选了这个，那就必须关闭UABEA，重新进入bundle，重新添加Sprite。一旦有Sprite勾选了，极大概率后面会不成功，亲测，两天都卡在这上面了。

<img width="1377" height="869" alt="image" src="https://github.com/user-attachments/assets/b57c11ce-8ffe-486f-afeb-e1528443bba9" />

接着用import dump导入修改后Sprite的json文件。


帧数少和方法二的后续步骤。修改assetbundle的json中的preloadtable和container，修改MONObehaviour的Sprite，修改animationclip的m_StreamedClip的行数、m_FrameCount的数值、m_StopTime数值、m_ValueArrayDelta里stop的数值，然后还有一些可以修改的属性设置我会写在最后，自行判断。

<img width="435" height="119" alt="image" src="https://github.com/user-attachments/assets/9506df46-38f3-46c5-acf6-3dbcc5042107" />
<img width="620" height="276" alt="image" src="https://github.com/user-attachments/assets/8d14cef2-2ac8-4555-8be9-2aece1a5baca" />
<img width="455" height="208" alt="image" src="https://github.com/user-attachments/assets/12e79b45-1af9-4ce2-a6e5-ff4e085141a3" />


Assetbundle

帧数少的，直接删除多余SpritePathID对应的preloadtable和container的结构，如下图的结构，每个Sprite对应的有三个下类结构，记得删干净。

<img width="1290" height="877" alt="image" src="https://github.com/user-attachments/assets/6a4a7b22-376d-44ba-a051-8a436c9b4123" />

帧数多的，则要添加相应的结构，preloadtable里Sprite的排列顺序是按照PathID的大小排列的，我一般是按着相应的顺序插入，不知道随意插入有没有影响，container的我则是插入。

这里讲解一下preloadtable与container的关系，如果不想看，也可以直接跳到下一步。preloadtable里加载的项包含了：一个fileid=1的项，这个项我认为是对应Assetbundle，两套Sprite和MONObehaviour，两个texture2D。

如果你去阅读代码，就会发现container里的preloadindex和preloadsize跟preloadtable的顺序是对应的。整个preloadtable被分为三组，组1是包含Assetbundle、一个texture2D和一套Sprite和monobehaviour，组2只有一个单独的texture2D，组3包含一个animationclip、一套MONObehaviour和Sprite。还有一点，这三个组在preloadtable出现的顺序每个文件中可能是不一样的。

然后在container中可见，组1没有出现Assetbundle的结构，组3只有animationclip的结构。(这说明他们的加载调用方式是有一定的，你们可以自己理解，这个不重要)
此时，就能index和size的关系了，size就是组中有几项，index就是在preloadtable出现的位置，记住，preloadtable的索引是从0开始的，因此需要在container中一项一项的区修改index和size，这里有一个口诀，这一组的index+size等于下一组的index，按这个去修改就行。

<img width="646" height="282" alt="image" src="https://github.com/user-attachments/assets/0e9cc4dc-f5a6-4619-8129-4bb065e1dca3" />

现在告诉你如何修改，首先找到size=1的组，它的index加或减你修改的帧数也有可能是加减二倍、即Sprite项数，需要看他出现的位置。接着，size最大的和sizeMAX-1的组，size加减你的帧数。接着，修改以上二者的index，index=0或index=1则的不需要修改，其中大的那个加减帧数。如果新增了Sprite的container结构，则记得修改使同一组中的index和size使其与其他Sprite的一致。此时，Assetbundle的修改就结束了,导入即可。


MONObehaviour和Animationclip

MONO的修改就简单,加减帧数就直接在下图中的列表中删除Sprite的对应的结构，加帧数要在列表的最后添加，这个就是动画帧的顺序。改完就结束了。

<img width="481" height="219" alt="image" src="https://github.com/user-attachments/assets/e25c32e1-8429-4057-96f8-b0671d1f1849" />

animation的修改相对复杂。

先讲解优化过的方法。首先先像MONO一样，修改原动画的Sprite列表。接着你可以直接导出新动画的animationclip，然后将修改过后的原动画的Sprite直接替换到新动画上。然后导入新动画修改后的animationclip。

原方法。

首先先像MONO一样，修改Sprite列表。

接着，找到m_StreamedClip列表。他的数组（array）的行数是跟你的帧数有关的，为帧数*7+2。这最后的两行不要修改，在它两上面开始修改至匹配即可，(我一般是改的因为这东西会影响内存占用，不过也问过AI，AI说可改可不改)。如果添加帧数，你可以直接从新动画的animationclip里获取，我看的几个同个游戏内的streamedclip基本上使用的都是同一个序列的，只是从头开始截取的行数不同，因此可以直接从帧数多的动画里复制过来。

<img width="460" height="256" alt="image" src="https://github.com/user-attachments/assets/c36e8a39-03bd-4682-b87f-b82c383d6138" />

再往下几行，就是framecount和stoptime。framecount修改为在Assetbundle中animation对应的preloadsize即可，stoptime改为stoptime/framecount(old)*framecount(new)。stoptime大概率为framecount/samplerate，可能有的游戏数值会有点特殊，比如我的游戏就是0.6666675而不是0.6333334，自行注意一下就好了。

<img width="478" height="600" alt="image" src="https://github.com/user-attachments/assets/39f2464f-4547-4c05-accc-8a83d913d0c6" />

最后修改m_ValueArrayDelta的stop，stop加减修改帧数即可。如我要加一帧，即18变1。以上就结束了。

<img width="436" height="220" alt="image" src="https://github.com/user-attachments/assets/cee54186-7be9-4c28-bfcb-ca0a1b382eb4" />


最后是一些可修改的属性。

m_MuscleClipSize，我一般将原动画的这个改为新动画的。

samplerate，我一般不改帧数。


脚本介绍

自动生成PathID，你只要输入一个container和相应的index和size，就会给你随机生成一个PathID。

Sprite PathID 重命名，能够修改你给与的Sprite的json文件中，引用Texture2D文件的PathID，用于简化修改。

图片顺序重命名，能够修改图片的名称，使其从00000开始连续递增，图片名称最好是只有一部分数字，不然可能会出事。作用：Name_00001、Name_00004、Name_00006。 修改为Name_00000、Name_00001、Name_00002。

剩余两个脚本专用性较强，可以不必关注。























