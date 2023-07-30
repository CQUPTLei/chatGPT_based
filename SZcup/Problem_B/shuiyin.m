close all;clear all;
img_1=imread('B.jpg');
img_2=rgb2gray(img_1);
img_sy=im2bw(img_2,210/255);
% img_sy=img_2;
figure;
imshow(img_sy);
title('ˮӡͼ��');
img_3=imread('B.jpg');
img_4=rgb2gray(img_3);
figure;imshow(img_4);
title('Ƕ��ˮӡǰ��ͼ��');
%��ˮӡͼ�����ؽ���2Dα�������
[M1 M2]=size(img_sy);
% bianhao=zeros(M1,M2);
% for m1=1:M1
%     for m2=1:M2
%         bianhao(m1,m2)=(m1-1)*M2+m2;%��ˮӡͼ�����к��е�˳����
%     end
% end
mishi=zeros(1,M1*M2);
wsjxl=randperm(M1*M2);%����α������У���Χ��1~M1*M2֮�䣬���ظ�
mishi=wsjxl;%����α������У���Ϊˮӡ�����ܳ�
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
%����ͼ����ˮӡͼ��ֿ�
%������ͼ��ֳ�8X8����ͼ��
%Ϊ��֤ˮӡͼ��������ͼ�����ͼ�����һ�£���ˮӡͼ��ֳɣ�8*M1/N1)X(8*M2/N2)����ͼ��
%Ϊ����ֿ飬������ͼ���ˮӡͼ���������о�Ϊ8��������
[N1 N2]=size(img_4);
img_5=[img_4,zeros(N1,4);zeros(7,504)];
img_rsave=[img_save,zeros(140,1);zeros(4,126)];
a=288/8;
b=504/8;
c=a*b;
x=8*144/288;
y=8*126/504;%x��y��ˮӡ��ͼ��Ĵ�С
kuai_sz=zeros(8,8,c);%������ά�������ڴ�����ͼ�����ͼ��
kuai_sy=zeros(x,y,c);%������ά�������ڴ�ˮӡͼ�����ͼ��
for m1=1:a
    for m2=1:b
        kuai_sz(:,:,(m1-1)*b+m2)=img_5(8*(m1-1)+1:8*m1,8*(m2-1)+1:8*m2);
        kuai_sy(:,:,(m1-1)*b+m2)=img_rsave(x*(m1-1)+1:x*m1,y*(m2-1)+1:y*m2);
    end
end
%����ͼ��ֿ���DCT�任
%ˮӡͼ��ֿ���DCT�任
img_dct_sz=zeros(8,8,c);%������ά�������ڴ�����ͼ��DCT�任���ͼ��
img_dct_sy=zeros(x,y,c);%������ά�������ڴ�ˮӡͼ��DCT�任���ͼ��
for i=1:c
    img_dct_sz(:,:,i)=dct2(kuai_sz(:,:,i));
    img_dct_sy(:,:,i)=dct2(kuai_sy(:,:,i));
end
%��ȡ����ͼ������Ƶϵ��
%DCT�任�����������ϼ��������Ͻǣ�Ϊ�������ȡͼ����е��м䲿��
img_szzp=zeros(x,y,c);
for i=1:c
    img_szzp(:,:,i)=img_dct_sz(3:6,4:5,i);
end
%ˮӡǶ��
%��ˮӡͼ��DCT�任���ͼ���������ͼ������Ƶͼ����Ӧ����
img_syqr=zeros(x,y,c);
syxs=20;
for i=1:c
    img_syqr(:,:,i)=img_szzp(:,:,i)+syxs*img_dct_sy(:,:,i);
end
%DCT��任
%��Ƕ��ˮӡ����Ƶͼ������ԭ������Ƶ�����ٷֿ������DCT�任
%�任���ͼ��鰴����˳����ϳ�һ������
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
img_7=uint8(img_6(1:N1,1:N2));%img_7ΪǶ��ˮӡ��ͼ��
figure;imshow(img_7);
title('Ƕ��ˮӡ���ͼ��');
%����������������������������������������������������������������������������������������������������������������������������������������������������
%����������������������������������������������������������������������������������������������������������������������������������������������������
%����Ϊˮӡ����ȡ
%ˮӡ��ȡ��ˮӡǶ��������
%�ȶ�Ƕ��ˮӡ��ͼ���ԭʼͼ��ֿ�DCT�任
%������Ƕ��ʱ��ԭʼͼ������˲����������ˮӡ��ȡʱҲӦ�Ȳ���
img_tq=uint8(img_6);%img_6���Ƕ�Ƕ��ˮӡ���ͼ������ͼ��
kuai_tq=zeros(8,8,c);
kuai_tq_dct=zeros(8,8,c);
for m1=1:a
    for m2=1:b
        kuai_tq(:,:,(m1-1)*b+m2)=img_tq(8*(m1-1)+1:8*m1,8*(m2-1)+1:8*m2);
        kuai_tq_dct(:,:,(m1-1)*b+m2)=dct2(kuai_tq(:,:,(m1-1)*b+m2));
    end
end
kuai_zj=zeros(8,8,c);%������ά�������ڴ�����ͼ�������ͼ��ֿ�DCT��Ĳ�
kuai_zj=kuai_tq_dct-img_dct_sz;%����ͼ��ֿ�DCT��ͼ����ԭʼͼ��ֿ�DCT������
kuai_zp=zeros(4,2,c);
img_tq_idct=zeros(4,2,c);
for i=1:c
    kuai_zp(:,:,i)=1/syxs*kuai_zj(3:6,4:5,i);%������õ���ͼ����ȡ�����е���Ƶ����
    img_tq_idct(:,:,i)=uint8(idct2(kuai_zp(:,:,i)));%��Ƶ��������DCT�任
end
%����DCT���ͼ�����ϳ�һ��ͼ��
img_tq=zeros(144,126);
for m1=1:a
    for m2=1:b
        img_tq(4*(m1-1)+1:4*m1,2*(m2-1)+1:2*m2)=img_tq_idct(:,:,b*(m1-1)+m2);
    end
end
img_tq=img_tq(1:140,1:125);
%���ñ�����ܳ���ȡˮӡͼ��
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
title('Ƕ��ˮӡͼ����������ȡ����ˮӡ');
%³������֤
%��ȡ��Ƕ��ˮӡ���ͼ�����������ȡ�Լ���ͼ��ü�����ȡ�ķ�������³������֤
% img_jz1=imnoise(img_7,'salt & pepper', 0.05);
% img_jz1=imnoise(img_7,'gaussian', 0,0.005);
img_8=imcrop(img_7,[1 1 249 149]);
img_jz1=[img_8,zeros(150,250);zeros(131,500)];
figure;imshow(img_jz1);
title('Ƕ��ˮӡ��ͼ������ͼ��');
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
title('��Ƕ��ˮӡ��ͼ�������ȡ����ˮӡ');






