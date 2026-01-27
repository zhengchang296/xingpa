该替换方式可跳过一帧一帧地更换图片及其图片对齐，同时可以自由的调整帧数。需要准备AssetStudio、UABEA，然后编辑json代码我用的是Visual Studio Code。AssetStudio主要用于查找目标bundle，UABEA主要用于修改bundle。

目前仅限于修改已有的动画文件，因为我还没有研究如何将每一帧的动画从Sprite里抠出来的代码。不过我目前有一个思路，就是直接将每一帧的图片拼成一整张图片，再去处理对应的json代码就行了，我记得好像要写rect代码。

首先，被替换的动画我称作原动画，你自己准备的动画我称作新动画。我这里有两种修改方式。

第一种，使用同个游戏的其他动画替换原动画。

用UABEA解包你新动画对应的bundle文件，将所有所有walk带数字的文件即Sprite文件export dump为json，texture2D文件的图片也要导出；原动画则需要导出assetbundle、animationclip、MONObehaviour的json文件。

<img width="1396" height="864" alt="image" src="https://github.com/user-attachments/assets/9a8f22ba-d854-4181-8570-43b6e841299a" />
<img width="1377" height="888" alt="image" src="https://github.com/user-attachments/assets/1c490d56-62cc-41fe-af84-066044ae4160" />

随后用右侧的插件修改原动画的Texture2D图片，Load导入新动画动画的精灵图即texture2D的图片。

<img width="755" height="614" alt="image" src="https://github.com/user-attachments/assets/0d037de4-2e94-481b-b533-9b401fcec8cd" />

最后，最痛苦的来了。修改新动画每个sprite文件的json文件，在里面找到pathID，替换为原动画动画bundle文件中Texture2D文件的pathID即路径ID。

<img width="629" height="392" alt="image" src="https://github.com/user-attachments/assets/1336fc8d-2328-4ed4-a75c-75e832684eac" />
<img width="293" height="855" alt="image" src="https://github.com/user-attachments/assets/3a9ddd22-bceb-42ac-aa1e-736367d256c4" />

接着将新动画每个sprite的json，import dump对应的原动画Sprite。如果你新动画的帧数小于原动画，记得按顺序将对应的Sprite导入，后直接删除多余的sprite文件即可，记得删数字最大的。如果新动画帧数大于原动画，那么有两种方法。一定要看完，后面还有步骤。

方法一，则需要修改你新动画相应json文件中的m_name。
这一步的对应关系比较复杂，就是你现选取你需要的帧数，如你想导入新动画的00000--00010、00021--00028这些帧，那就修改新动画的名称中带相应数字的json文件，使得里面的m_name变成连续的，即将00021--00028中n_name的数字改为00011--00018，所有文件的n_name必须保持连续，这样动画运行过程中才能在相应的帧数中读取

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

接着用import dump导入修改后的json文件。


















