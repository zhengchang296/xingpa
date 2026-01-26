该替换方式可跳过一帧一帧地更换图片及其图片对齐，同时可以自由的调整帧数。

目前仅限于修改已有的动画文件，因为我还没有研究如何将每一帧的动画从Sprite里抠出来的代码。不过我目前有一个思路，就是直接将每一帧的图片拼成一整张图片，再去处理对应的json代码就行了，我记得好像要写rect代码。

第一步、UABEA解包你想要替换成的动画对应的bundle文件，将所有所有walk带数字的文件导出转储为json格式，需要被替换的动画的bundle文件则需要导出Texture2D的json

<img width="1219" height="881" alt="image" src="https://github.com/user-attachments/assets/84ba565c-4feb-41e3-b6bb-c52cf398ca4f" />

随后用右侧的插件修改Texture2D图片，Load导入替换动画的精灵图。

<img width="755" height="614" alt="image" src="https://github.com/user-attachments/assets/0d037de4-2e94-481b-b533-9b401fcec8cd" />




第三步、是最痛苦的一步。修改每个sprite文件导出的json文件找到pathID，替换为被替换动画bundle文件中Texture2D文件的pathID即路径ID。

<img width="629" height="392" alt="image" src="https://github.com/user-attachments/assets/1336fc8d-2328-4ed4-a75c-75e832684eac" />
<img width="293" height="855" alt="image" src="https://github.com/user-attachments/assets/3a9ddd22-bceb-42ac-aa1e-736367d256c4" />

接着将每个sprite的json导入。如果你导入的动画的帧数小于原动画，记得按顺序将对应的Sprite导入，后直接删除多余的sprite文件，记得删数字最大的。如果导入帧数大于原动画，那么有两种方法。

方法一，则需要修改你相应json文件中的m_name。
这一步的对应关系比较复杂，就是你现选取你需要的帧数，如00000--00010、00021--00028，修改新动画的名称中带相应数字的json文件，里面的m_name改呈连续的，即将00021--00028中n_name的数字改为00011--00018，所有文件的n_name必须保持连续，这样动画运行过程中才能在相应的帧数中读取

<img width="431" height="280" alt="image" src="https://github.com/user-attachments/assets/abbe562e-837a-4749-ba17-72a54b15541b" />

方法二，则是让你在bundle文件中添加Sprite项。
