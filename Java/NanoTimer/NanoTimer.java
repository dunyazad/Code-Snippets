package com.imc;

import java.util.LinkedList;

public class NanoTimer {

    long mInterval = 13333333;
    long mEventPerSecond = 75;
    boolean mThreadDone = false;
    Thread mThread;
    LinkedList<Callback> mCallbacks = new LinkedList<>();

    public NanoTimer(long eventPerSecond) {
        mEventPerSecond = eventPerSecond;
        mInterval = 1000000000 / mEventPerSecond;
    }

    public void Start() {
        if (mThread == null) {
            mThread = new Thread() {
                public void run() {
                    long lastTime = System.nanoTime();
                    while (mThreadDone == false) {
                        long now = System.nanoTime();
                        long nextTime = lastTime + mInterval;
                        while (now < nextTime) {
                            try {
                                Thread.sleep(1);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                            now = System.nanoTime();
                        }

                        long delta = now - lastTime;
                        for (Callback callback : mCallbacks) {
                            callback.OnTimer(delta);
                        }
                    }
                }
            };
        }
    }

    public void OnTimer(Callback callback) {
        mCallbacks.addLast(callback);
    }

    public interface Callback {
        void OnTimer(long timeDelta);
    }
}
