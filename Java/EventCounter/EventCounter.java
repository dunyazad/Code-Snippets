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

public class EventCounter {
    private static EventCounter sinstance = null;

    private static HashMap<String, EventCounterElement> sEventCounterElements;
    private EventCounter() {
        sEventCounterElements = new HashMap<>();
    }

    public static void Event(String key, String message) {
        if(sinstance == null) {
            sinstance = new EventCounter();
        }

        if(sEventCounterElements.containsKey(key) == false) {
            sEventCounterElements.put(key, new EventCounterElement());
        }

        Log.i(key, sEventCounterElements.get(key).Event(message));
    }
}
