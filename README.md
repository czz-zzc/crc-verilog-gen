本文以CRC16为例进行64bit并行电路实现原理的推导过程。
CRC16(0x1B09)，生成多项式：

<img width="193" alt="image" src="https://github.com/user-attachments/assets/06c43703-26bd-47a6-b3fa-dfb1239972b0">

生成多项式对应的串行实现电路如下：

<img width="500" alt="image" src="https://github.com/user-attachments/assets/c8580ca6-2b96-4392-a0ee-a15262f125d2">

根据串行电路可得到如下矩阵方程，该方程表示触发器X_0~X_15，在t时刻和t+1时刻的关系。

<img width="350" alt="image" src="https://github.com/user-attachments/assets/d6810383-5d77-4489-84b3-61cf1a5886ec">

令：

<img width="368" alt="image" src="https://github.com/user-attachments/assets/35681cb8-8bbf-414b-96fd-86c8dafaf88d">

则

<img width="155" alt="image" src="https://github.com/user-attachments/assets/fece8875-6082-4966-830a-08d2b2adca46">

由此可推得

<img width="239" alt="image" src="https://github.com/user-attachments/assets/40b10a55-d8ef-4f59-a744-7deccdc0392c">

又由于F矩阵得特殊性，可得

<img width="160" alt="image" src="https://github.com/user-attachments/assets/e6015309-55de-4a0c-a01e-5ce78ef44acb">

则

<img width="176" alt="image" src="https://github.com/user-attachments/assets/09a25849-0267-49bc-8b1f-17623222a148">

继续递推

<img width="196" alt="image" src="https://github.com/user-attachments/assets/faaa5f4f-5812-45ab-85e0-7e716f60a378">

继续

<img width="280" alt="image" src="https://github.com/user-attachments/assets/3a4d65b8-e00e-4e6b-b1d9-74e8ddbc9d24">

最后得出

<img width="347" alt="image" src="https://github.com/user-attachments/assets/26fd3097-ae38-40d7-b8c8-79d894a02de0">

推导结束


注：利用该方法可推导任一位宽得CRC计算，但硬件实现时需要注意增加并行度的同时会带来逻辑级数的增加，即会增加路径延迟。


