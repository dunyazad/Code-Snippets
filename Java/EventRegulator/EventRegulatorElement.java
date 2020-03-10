package com.imc;
import java.util.concurrent.TimeUnit;

public class EventRegulatorElement {
    long mLastTime = System.nanoTime();
    long mInterval = 13333333;
    long mEventPerSecond = 75;

    public EventRegulatorElement(long eventPerSecond) {
        mEventPerSecond = eventPerSecond;
        mInterval = 1000000000 / mEventPerSecond;
    }

    public long Event(long eventPerSecond) {
        mEventPerSecond = eventPerSecond;
        mInterval = 1000000000 / mEventPerSecond;

//        long now = System.nanoTime();
//        long nextTime = mLastTime + mInterval;
//        while(now < nextTime) {
//            try {
//                Thread.sleep(1);
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
//            now = System.nanoTime();
//        }
//
//        long delta = now - mLastTime;
//        mLastTime = now;
//
//        return delta;

        mLastTime += 1000 * 1000 * 1000 / mEventPerSecond;
        long next = mLastTime - System.nanoTime();
        try {
            if (next < 0) {
                // Exceed time!
                mLastTime = System.nanoTime();
            } else {
                TimeUnit.NANOSECONDS.sleep(next);
            }
        } catch (InterruptedException e) {
        }

        long delta = System.nanoTime() - mLastTime;
        //mLastTime = System.nanoTime();

        return delta;



//        long now = System.nanoTime();
//        long delta = now - mLastTime;
//        mLastTime = now;
//
//        long toSleepM = mInterval - delta;
//        long toSleepN = (mInterval - ((mInterval / 1000000) * 1000000)) - delta;
//        if(toSleepN < 0) toSleepN = 0;
//        if(toSleepM >= 0) {
//            try {
//                Thread.sleep(toSleepM / 1000000, (int)toSleepN / 1000000);
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
//        }
    }
}
