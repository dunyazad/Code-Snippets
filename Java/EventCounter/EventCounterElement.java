package com.imc;

import android.util.EventLog;
import android.util.Log;
import android.util.Pair;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class EventCounterElement {
    public EventCounterElement() {
    }

    long mLastTime = -1;
    long mLastTimeSecond = -1;
    long mCountPerSecond = -1;
    long mMinDelta = 999999999;
    long mMaxDelta = 0;
    long mSumDelta = -1;

    public String Event(String message) {
        long now = System.nanoTime();

        String log = "";

        long delta = 0;

        if(mLastTime != -1) {
            delta = now - mLastTime;
            mSumDelta += delta;
            mCountPerSecond++;

            if(mMinDelta > delta) mMinDelta = delta;
            if(mMaxDelta < delta) mMaxDelta = delta;

            log += String.format("%.4f ms", (double)delta / 1000000.0);
        }
        mLastTime = now;

        if(now - mLastTimeSecond > 1000000000) {
            log += String.format(
                    "        min : %.4f ms, max : %.4f ms, average : %.4f ms, count : %d",
                    (double)mMinDelta / 1000000.0,
                    (double)mMaxDelta / 1000000.0,
                    (double)mSumDelta / (double)mCountPerSecond / 1000000.0,
                    mCountPerSecond);

            mCountPerSecond = 0;
            mMinDelta = 99999999;
            mMaxDelta = 0;
            mSumDelta = 0;

            mLastTimeSecond = now;
        }

        if(message.isEmpty() == false) {
            log += " | ";
            log += message;
        }

        return log;
    }
}
