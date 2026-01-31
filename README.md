该替换方式可跳过一帧一帧地更换图片及其图片对齐，同时可以自由的调整帧数。需要准备AssetStudio、UABEA，然后编辑json代码我用的是Visual Studio Code。AssetStudio主要用于查找目标bundle，UABEA主要用于修改bundle。对于部分脚本的使用会在最后讲解。建议先完全阅读完一遍教程，能有个初步印象再开始进行修改。

我这里有两种修改方式。分为同个游戏的其他动画替换原动画和自制动画。

这里介绍使用同个游戏的其他动画替换原动画的方式，自制动画的方式在整理完会导入到其他分支的readme。


首先，被替换的动画我称作原动画，你自己准备的动画我称作新动画。


新动画，用UABEA解包你新动画对应的bundle文件，将所有所有walk带数字的文件即Sprite文件和上面type为Animationclip的文件，export dump为json，texture2D文件的图片使用plugins中的export导出；原动画则需要导出assetbundle、animationclip、MONObehaviour的json文件。

<img width="1377" height="664" alt="image" src="https://github.com/user-attachments/assets/5470e9b4-ad11-422c-88a2-d0931e268010" />
<img width="1377" height="888" alt="image" src="https://github.com/user-attachments/assets/1c490d56-62cc-41fe-af84-066044ae4160" />

随后，使用UABEA打开原动画的bundle，用右侧的插件修改原动画的Texture2D图片，Load导入新动画动画的精灵图即texture2D的图片。

<img width="755" height="614" alt="image" src="https://github.com/user-attachments/assets/0d037de4-2e94-481b-b533-9b401fcec8cd" />

最后，最痛苦的来了。修改新动画每个sprite文件的json文件，在里面找到pathID，替换为原动画bundle文件中Texture2D文件的pathID即路径ID。这步已被相对简化，对应PathID的修改可使用提供的脚本修改。

<img width="1121" height="80" alt="image" src="https://github.com/user-attachments/assets/b58a0991-eeed-480e-b075-7e0f536671ea" />

例如，上图是原动画Texture2D文件的PathID，则将下图中的PathID改为上图的PathID即可。小提醒，选中相应的文件后，可以直接在的UABEA右侧复制PathID。

<img width="629" height="392" alt="image" src="https://github.com/user-attachments/assets/1336fc8d-2328-4ed4-a75c-75e832684eac" />


接着将新动画每个sprite的json，import dump入对应的原动画Sprite。例如，新动画的walk_00001,则导入原动画的walk_00001。如果新原动画的Sprite数量相等，则不需要进行帧数的修改，不需要修改Assetbundle、animationclip、monobehaviour的代码。只需要导入对应的Sprite后，保存就完成了。如果帧数不等，则需根据下面的方法修改后再往后做。一定要看完，帧数少和方法二的这一步，后面还有步骤。

命名这一步为  调节帧数

如果你新动画的帧数小于原动画，记得按顺序将对应的Sprite导入，后直接删除多余的sprite文件即可，记得删数字最大的。例如十二帧，则保留00000--00011，删除（remove）大于00011的Sprite。减少帧数的调节帧数步骤后面还有，需要往后看

<img width="1377" height="664" alt="image" src="https://github.com/user-attachments/assets/1e3e3764-28c0-42a4-9e05-6975ab317fef" />


如果新动画帧数大于原动画，那么有两种方法。

方法一，则需要你根据原动画的Sprite项的数量、即帧数，在新动画中选择相同数量是Sprite。如果这样做，就会让新动画的帧数减少。
这一步的对应关系可能有点复杂，首先，假定你的原动画只有十九帧。然后，你需要选定在新动画00000--00028这些帧中你想要导入的帧数。例如，00000--00010，00021--00028，那么你就根据从小到大的顺序导入到原动画的00000--00018里即可。方法一调节帧数的这一步到这里就结束了。方法一在选取想要保留的帧数后，可以不需要修改Assetbundle、animationclip、monobehaviour的代码。跟帧数相等的一样，只需要导入对应的Sprite即可。


方法二，则是让你在原动画bundle中添加Sprite项。我比较推荐这一种，因为方法二与减帧数，这两种方法是真的调节帧数。

以下讲解增加帧数的方法，如果需要减少帧数，则进行相应的反处理即可。

首先，获得原动画的Sprite的container码。我一般是进到原动画的assetbundle里，复制图中的first获得的，如果是按我的方法，则需要的是重复出现的first值，至于原因，则会在后文讲解。

<img width="282" height="557" alt="image" src="https://github.com/user-attachments/assets/43b16734-4223-40b2-b757-50641fbd2c62" />
<img width="796" height="883" alt="image" src="https://github.com/user-attachments/assets/789e82a8-2c0c-4a27-a0ac-a1d08084156e" />



复制后使用自动PathID脚本，输入first、preloadindex、preloadsize值，后得到一个PathID和两类代码。关于index和size会在后文介绍，这里随便输入也可以。在熟练后，可以在这一步同时生成出index和size，会相应减轻一点后面的工作量。

<img width="1483" height="762" alt="image" src="https://github.com/user-attachments/assets/6afb48d9-0f93-44a6-bf6e-6d88ba5ccc37" />


接着，便开始添加Sprite项。使用UABEA左上角file的add，输入PathID，type栏输入Sprite或213都可以，MONO栏不变。

划重点，那个fill Asset with 00s一定不能勾选，如果加入的Sprite勾选了这个，那就必须关闭UABEA，重新进入bundle，重新添加Sprite。一旦有Sprite勾选了，极大概率后面会不成功，亲测，两天都卡在这上面了。

<img width="1377" height="869" alt="image" src="https://github.com/user-attachments/assets/b57c11ce-8ffe-486f-afeb-e1528443bba9" />

接着用import dump导入修改后Sprite的json文件。


以下修改都是针对原动画文件的修改，需要修改assetbundle的json中的preloadtable和container，修改MONObehaviour的Sprite，修改animationclip的m_StreamedClip的行数、m_FrameCount的数值、m_StopTime数值、m_ValueArrayDelta里stop的数值，然后还有一些可以修改的属性设置我会写在最后，自行判断。

<img width="435" height="119" alt="image" src="https://github.com/user-attachments/assets/9506df46-38f3-46c5-acf6-3dbcc5042107" />
<img width="620" height="276" alt="image" src="https://github.com/user-attachments/assets/8d14cef2-2ac8-4555-8be9-2aece1a5baca" />
<img width="455" height="208" alt="image" src="https://github.com/user-attachments/assets/12e79b45-1af9-4ce2-a6e5-ff4e085141a3" />


Assetbundle文件部分

需要添加相应的结构，preloadtable里Sprite的排列顺序是按照PathID的大小排列的，我一般是按着相应的顺序插入，不知道随意插入有没有影响，container的我则是随意插入。

注意，preloadtable这里需要插入两次下图的第一个json结构。我推荐一种方法就是按PathID大小排序后，复制新增项上面那项Sprite的PathID，然后到VSC（json文件编辑器）中查找该PathID，然后在查找到的结构的下面粘贴随机生成PathID的第一个json结构，查找到的前两项的下面都要粘贴这个结构，原因会在后面讲。然后第三项，则粘贴第二个json结构。

<img width="1377" height="664" alt="image" src="https://github.com/user-attachments/assets/bfd29fde-1eb0-4034-bf5f-27d94350ea5f" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/55d9f057-61e7-4933-a9c1-1e4c12032aad" />



这里讲解一下preloadtable与container的关系和index、size的赋值。可以阅读到preloadtable里加载的项包含了：一个fileid=1的项，这个项我认为是对应Assetbundle，此外还有两套Sprite和MONObehaviour，两个texture2D和一个animationclip。

如果你去阅读代码，就会发现container里的preloadindex和preloadsize跟preloadtable的顺序是对应的。整个preloadtable被分为三组，组1是包含Assetbundle、一个texture2D和一套Sprite和monobehaviour，即size=Sprite数+3，组2只有一个单独的texture2D，即size=1，组3包含一个animationclip、一套MONObehaviour和Sprite，即size=Sprite数+2。还有一点，这三个组在preloadtable出现的顺序每个文件中可能是不一样的，因此会导致index的一定变化。

然后在container中可见，组1虽然多次重复，没有出现含有Assetbundle的PathID结构：组3虽然包含了上面提到的多个东西，但可以见到只出现了animationclip的PathID结构。(这说明他们的加载调用方式是一定的，ASB调用对象包括自己、一套Sprite和monobehaviour、一个Texture2D，ANC调用对象包括自己、一套Sprite和monobehaviour。你们可以自己理解，理解不了可能也影响不大)

此时，就能推测出index和size的关系了，size就是组中有几项，index就是在该组第一项在preloadtable中出现的位置，从0开始。可以理解为size是自变量，index是因变量。size的值与Sprite有关，组1size=Sprite+3，组3size=Sprite+2，而由于组2不包含Sprite，只有一项Texture，则size=1.

因此调节帧数后，需要在container中一项一项的去修改index和size，这里有一个口诀，上一组的index+size等于下一组的index，按这个去修改就行。记住一点，preloadtable的索引是从0开始数的。

<img width="646" height="282" alt="image" src="https://github.com/user-attachments/assets/0e9cc4dc-f5a6-4619-8129-4bb065e1dca3" />

现在告诉你如何修改，因为前文提到过，三个组在preloadtable出现的顺序不一定相同，所有需要先观察三组的index和size。

首先找到size=1的组，若它的index=0，则不修改；若index是在三组的index中最大，则增加二倍新增的Sprite项数，若index为中等大小值，则增加一倍新增的Sprite项数。

接着，找到size最大的和sizeMAX-1的组，size增加新增的Sprite项数。接着，修改以上二者的index，index=0或index=1则的不需要修改，其中index大的那个增加新增Sprite项数。

总之，规律就是上一组的index+size=下一组的index。

解释一下原因，因为在原本的preloadtable中，三个组已经排好了顺序，但是因为我们新增了Sprite，在preloadtable插入了两次这两次插入就是在组1、组3中各插入了新增Sprite的结构，这时候，就会导致preloadtable的总索引增大，组1、组3的含量增大，即size增大。因此会导致排在后面的两组第一项出现的位置后移，就会导致他们的index发生相应的增加。

如果想要减少帧数，则在Assetbundle进行反处理即可。


MONObehaviour和Animationclip部分

MONO的修改就简单,加减帧数就直接在下图中的列表中删除Sprite的对应的结构，加帧数要在列表的最后添加，这个就是动画帧的顺序，一定要按照新动画的帧顺序添加。改完就结束了。

<img width="481" height="219" alt="image" src="https://github.com/user-attachments/assets/e25c32e1-8429-4057-96f8-b0671d1f1849" />

animation的修改相对复杂。

先讲解优化过的方法。首先先像MONO一样，修改原动画的Sprite列表，这里的名称为pptrCurveMapping。接着你可以直接导出新动画的animationclip，然后将修改过后的原动画的pptrCurveMapping列表，直接覆盖到到新动画上。然后将新动画修改后的animationclip导入原动画的animationclip项。

<img width="690" height="899" alt="image" src="https://github.com/user-attachments/assets/0a230a67-ef5c-4dd7-ba7c-b7de18c25dfe" />

原方法。

首先先像MONO一样，修改Sprite列表，这里的名称为pptrCurveMapping。

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

动画解包，可用于解出每一帧图片，可用于预览，需要安装pillow。此脚本教程见附件，来源与狐工坊。























