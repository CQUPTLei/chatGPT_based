close all;clear all;
img_1=imread('B.jpg');
img_2=rgb2gray(img_1);
img_sy=im2bw(img_2,210/255);
% img_sy=img_2;
figure;
imshow(img_sy);
title('水印图像');
img_3=imread('B.jpg');
img_4=rgb2gray(img_3);
figure;imshow(img_4);
title('嵌入水印前的图像');
%对水印图像像素进行2D伪随机排列
[M1 M2]=size(img_sy);
% bianhao=zeros(M1,M2);
% for m1=1:M1
%     for m2=1:M2
%         bianhao(m1,m2)=(m1-1)*M2+m2;%对水印图像按先行后列的顺序编号
%     end
% end
mishi=zeros(1,M1*M2);
wsjxl=randperm(M1*M2);%产生伪随机序列，范围在1~M1*M2之间，无重复
mishi=wsjxl;%保存伪随机序列，此为水印检测的密匙
re_wsjxl=zeros(M1,M2);
for m1=1:M1
    for m2=1:M2
        re_wsjxl(m1,m2)=wsjxl(1,(m1-1)*M2+m2);
    end
end
img_save=zeros(M1,M2);
for m1=1:M1
    for m2=1:M2
        b=mod(re_wsjxl(m1,m2),M2);
        if b==0
            a=(re_wsjxl(m1,m2)-b)/M2;
            b=M2;
        else
            a=(re_wsjxl(m1,m2)-b)/M2+1;
        end
        img_save(m1,m2)=img_sy(a,b);
    end
end
%宿主图像与水印图像分块
%把宿主图像分成8X8的子图像
%为保证水印图像与宿主图像的子图像块数一致，把水印图像分成（8*M1/N1)X(8*M2/N2)的子图像
%为方便分块，把宿主图像和水印图像补零至行列均为8的整数倍
[N1 N2]=size(img_4);
img_5=[img_4,zeros(N1,4);zeros(7,504)];
img_rsave=[img_save,zeros(140,1);zeros(4,126)];
a=288/8;
b=504/8;
c=a*b;
x=8*144/288;
y=8*126/504;%x、y是水印子图像的大小
kuai_sz=zeros(8,8,c);%建立三维向量用于存宿主图像的子图像
kuai_sy=zeros(x,y,c);%建立三维向量用于存水印图像的子图像
for m1=1:a
    for m2=1:b
        kuai_sz(:,:,(m1-1)*b+m2)=img_5(8*(m1-1)+1:8*m1,8*(m2-1)+1:8*m2);
        kuai_sy(:,:,(m1-1)*b+m2)=img_rsave(x*(m1-1)+1:x*m1,y*(m2-1)+1:y*m2);
    end
end
%宿主图像分块做DCT变换
%水印图像分块做DCT变换
img_dct_sz=zeros(8,8,c);%建立三维向量用于存宿主图像DCT变换后的图像
img_dct_sy=zeros(x,y,c);%建立三维向量用于存水印图像DCT变换后的图像
for i=1:c
    img_dct_sz(:,:,i)=dct2(kuai_sz(:,:,i));
    img_dct_sy(:,:,i)=dct2(kuai_sy(:,:,i));
end
%提取宿主图像块的中频系数
%DCT变换后能量基本上集中在左上角，为简单起见，取图像块中的中间部分
img_szzp=zeros(x,y,c);
for i=1:c
    img_szzp(:,:,i)=img_dct_sz(3:6,4:5,i);
end
%水印嵌入
%把水印图像DCT变换后的图像块与宿主图像块的中频图像块对应叠加
img_syqr=zeros(x,y,c);
syxs=20;
for i=1:c
    img_syqr(:,:,i)=img_szzp(:,:,i)+syxs*img_dct_sy(:,:,i);
end
%DCT逆变换
%用嵌入水印的中频图像块代替原来的中频部分再分块进行逆DCT变换
%变换后把图像块按行列顺序组合成一个整体
img_idct=zeros(8,8,c);
img_dct_sz1=zeros(8,8,c);
for i=1:c
    d=[img_dct_sz(3:6,1:3,i),img_syqr(:,:,i),img_dct_sz(3:6,6:8,i)];
    img_dct_sz1(:,:,i)=[img_dct_sz(1:2,:,i);d;img_dct_sz(7:8,:,i)];
    img_idct(:,:,i)=idct2(img_dct_sz1(:,:,i));
end
img_6=zeros(288,504);
for i=1:c
    f=mod(i,b);
    if f==0
        e=i/b;
        f=b;
    else
        e=(i-f)/b+1;
    end
    img_6(8*(e-1)+1:8*e,8*(f-1)+1:8*f)=img_idct(:,:,i);
end
img_7=uint8(img_6(1:N1,1:N2));%img_7为嵌入水印的图像
figure;imshow(img_7);
title('嵌入水印后的图像');
%··········································································
%··········································································
%以下为水印的提取
%水印提取是水印嵌入的逆过程
%先对嵌入水印的图像和原始图像分块DCT变换
%由于在嵌入时对原始图像进行了补零操作，故水印提取时也应先补零
img_tq=uint8(img_6);%img_6即是对嵌入水印后的图像补零后的图像
kuai_tq=zeros(8,8,c);
kuai_tq_dct=zeros(8,8,c);
for m1=1:a
    for m2=1:b
        kuai_tq(:,:,(m1-1)*b+m2)=img_tq(8*(m1-1)+1:8*m1,8*(m2-1)+1:8*m2);
        kuai_tq_dct(:,:,(m1-1)*b+m2)=dct2(kuai_tq(:,:,(m1-1)*b+m2));
    end
end
kuai_zj=zeros(8,8,c);%建立三维向量用于存待检测图像和宿主图像分块DCT后的差
kuai_zj=kuai_tq_dct-img_dct_sz;%待测图像分块DCT后图像与原始图像分块DCT后作差
kuai_zp=zeros(4,2,c);
img_tq_idct=zeros(4,2,c);
for i=1:c
    kuai_zp(:,:,i)=1/syxs*kuai_zj(3:6,4:5,i);%把作差得到的图像提取出其中的中频部分
    img_tq_idct(:,:,i)=uint8(idct2(kuai_zp(:,:,i)));%中频部分作逆DCT变换
end
%把逆DCT后的图像块组合成一个图像
img_tq=zeros(144,126);
for m1=1:a
    for m2=1:b
        img_tq(4*(m1-1)+1:4*m1,2*(m2-1)+1:2*m2)=img_tq_idct(:,:,b*(m1-1)+m2);
    end
end
img_tq=img_tq(1:140,1:125);
%利用保存的密匙提取水印图像
re_sy=zeros(M1,M2);
for m1=1:M1
    for m2=1:M2
        i=re_wsjxl(m1,m2);
        g=mod(i,M2);
        if g==0
            h=i/M2;
            g=M2;
        else
            h=(i-g)/M2+1;
        end
        re_sy(h,g)=img_tq(m1,m2);
    end
end
figure;imshow(logical(re_sy));
% figure;imshow(uint8(re_sy));
title('嵌入水印图像不做处理提取出的水印');
%鲁棒性验证
%采取对嵌入水印后的图像加噪声再提取以及对图像裁剪后提取的方法来做鲁棒性验证
% img_jz1=imnoise(img_7,'salt & pepper', 0.05);
% img_jz1=imnoise(img_7,'gaussian', 0,0.005);
img_8=imcrop(img_7,[1 1 249 149]);
img_jz1=[img_8,zeros(150,250);zeros(131,500)];
figure;imshow(img_jz1);
title('嵌入水印的图像处理后的图像');
img_tq_1=uint8([img_jz1,zeros(281,4);zeros(7,504)]);
kuai_tq_1=zeros(8,8,c);
kuai_tq_dct_1=zeros(8,8,c);
for m1=1:a
    for m2=1:b
        kuai_tq_1(:,:,(m1-1)*b+m2)=img_tq_1(8*(m1-1)+1:8*m1,8*(m2-1)+1:8*m2);
        kuai_tq_dct_1(:,:,(m1-1)*b+m2)=dct2(kuai_tq_1(:,:,(m1-1)*b+m2));
    end
end
kuai_zj_1=zeros(8,8,c);
kuai_zj_1=kuai_tq_dct_1-img_dct_sz;
kuai_zp_1=zeros(4,2,c);
img_tq_idct_1=zeros(4,2,c);
for i=1:c
    kuai_zp_1(:,:,i)=1/syxs*kuai_zj_1(3:6,4:5,i);
    img_tq_idct_1(:,:,i)=uint8(idct2(kuai_zp_1(:,:,i)));
end
img_tq_1=zeros(144,126);
for m1=1:a
    for m2=1:b
        img_tq_1(4*(m1-1)+1:4*m1,2*(m2-1)+1:2*m2)=img_tq_idct_1(:,:,b*(m1-1)+m2);
    end
end
img_tq_1=img_tq_1(1:140,1:125);
re_sy_1=zeros(M1,M2);
for m1=1:M1
    for m2=1:M2
        i=re_wsjxl(m1,m2);
        g=mod(i,M2);
        if g==0
            h=i/M2;
            g=M2;
        else
            h=(i-g)/M2+1;
        end
        re_sy_1(h,g)=img_tq_1(m1,m2);
    end
end
% figure;imshow(uint8(re_sy_1));
figure;imshow(logical(re_sy_1));
title('对嵌入水印的图像处理后提取出的水印');






