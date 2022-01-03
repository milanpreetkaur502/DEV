#include "opencv2/core/utility.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/video/tracking.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgcodecs.hpp"

#include <iostream>
#include <ctype.h>

using namespace cv;
using namespace std;

int main(int, char**)
{
    Mat frame1, frame2, diff1, gray1, blur1, thresh1;
    char str[] = "status : insect captured";
    char filename[100] = {0};
    
    vector<vector<Point>> contours1;
    //vector<Vec4i> hierarchy;
    
    //--- INITIALIZE VIDEOCAPTURE
    VideoCapture cap;
    // open the default camera using default API
    // cap.open(0);
    // OR advance usage: select any API backend
    int deviceID = 0;             // 0 = open default camera
    int apiID = cv::CAP_ANY;      // 0 = autodetect default API
    // open selected camera using selected API
    cap.open(deviceID, apiID);
    // check if we succeeded
    if (!cap.isOpened()) {
        cerr << "ERROR! Unable to open camera\n";
        return -1;
    }
    
    int j = 0;
    for (;;)
    {
        // wait for a new frame from camera and store it into 'frame'
        cap.read(frame1);
        // check if we succeeded
        if (frame1.empty()) {
            cerr << "ERROR! blank frame grabbed\n";
            break;
        }
        
        cap.read(frame2);
        // check if we succeeded
        if (frame2.empty()) {
            cerr << "ERROR! blank frame grabbed\n";
            break;
        }
        
        absdiff(frame1, frame2, diff1);
        
        cvtColor( diff1, gray1, COLOR_BGRA2GRAY );
        
        GaussianBlur(gray1, blur1, Size(5, 5), 0);
        
        threshold(blur1, thresh1, 40,255, THRESH_BINARY);
        
        findContours(thresh1, contours1, RETR_TREE, CHAIN_APPROX_SIMPLE);
        
        vector<Rect> boundRect( contours1.size() );
        
        
        for(int i=0; i<contours1.size();i++)
        {
        	boundRect[i] = boundingRect( Mat(contours1[i]) );
        	if(contourArea(contours1[i]) <4000)
        		continue;
        		
        	Point p1(boundRect[i].x, boundRect[i].y);
        	Point p2(boundRect[i].x + boundRect[i].width, boundRect[i].y + boundRect[i].height);
        	
        	
        	rectangle(frame1, p1, p2, Scalar(0, 255, 0), 2);
        	
        	putText(frame1, str, Point(50,50), FONT_HERSHEY_SIMPLEX, 1, Scalar(0,0,255), 3);
        	
        	memset(filename, 0, 100);
        	sprintf(filename, "/home/nitansh/motion_detection_images/image %d %d .jpg",j, i); 
        	
        	imwrite(filename, frame1);
        	
        	
        	printf("\nimage being captured %d", i);
        	
        }
        
        j++;
        
        

    }
    
    return 0;
}
