#include <opencv2\core.hpp>
#include <opencv2\highgui.hpp>
#include "HiddenWatermark.h"
using namespace cv;
int main()
{
	HiddenWatermark hiddenWatermark;
	hiddenWatermark.addWatermark("C:\\1.jpg","C:\\1.jpg","C:\\2.jpg"); //���ˮӡ
	hiddenWatermark.extWatermark("C:\\2.jpg","C:\\2.jpg","C:\\3.jpg"); //��ȡˮӡ
	return 0;
}
