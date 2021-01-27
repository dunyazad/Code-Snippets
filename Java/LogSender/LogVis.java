package com.imc.ixrclient;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.net.URISyntaxException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;

public class LogVis {
    private static String sIP = "192.168.3.170";
    private static int sPort = 12127;
    private static InetAddress sInetAddress = null;
    private static DatagramSocket sDatagramSocket = null;
    private static boolean sFirstTime = true;

    public LogVis() {
    }

    public static class KeyValuePair {
        public String key;
        public Object value;

        public KeyValuePair(String k, Object v) {
            key = k;
            value = v;
        }
    }

    private static HashMap<String, ArrayList<KeyValuePair>> sLogs = new HashMap<>();
    private static HashMap<String, Long> sLogIndices = new HashMap<String, Long>();
    private static HashMap<String, Long> sLogLastTime = new HashMap<String, Long>();

    private static String sKey = "";

    public static void BeginLogUnit(String key) {
        sKey = key;

        ArrayList<KeyValuePair> units;
        if (sLogs.containsKey(sKey) == false) {
            units = new ArrayList<KeyValuePair>();
            sLogs.put(sKey, units);
        } else {
            units = sLogs.get(sKey);
            units.clear();
        }

        if (sLogIndices.containsKey(sKey) == false) {
            sLogIndices.put(sKey, 0l);
        }

        if(sLogLastTime.containsKey(sKey) == false) {
            sLogLastTime.put(sKey, 0l);
        }
    }

    public static void AddLog(String key, Object obj) {
        sLogs.get(sKey).add(new KeyValuePair(key, obj));
    }

    public static void EndLog(String key) {
        if(sFirstTime) {
            sFirstTime = false;

            SendLog("ixr-client: " + getIP());
        }

        if (sLogs.containsKey(key)) {
            JSONObject jo = new JSONObject();
            {
                JSONObject header = new JSONObject();
                try {
                    long lastLogTime = sLogLastTime.get(sKey);
                    long now = System.nanoTime();
                    sLogLastTime.put(sKey, now);
                    header.put("log time", now);
                    header.put("log time diff", now - lastLogTime);
                    header.put("log index", sLogIndices.get(key));
                    header.put("name", sKey);
                    sLogIndices.put(key, sLogIndices.get(key) + 1);
                    jo.put("header", header);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            {
                JSONObject data = new JSONObject();
                sLogs.get(key).forEach((kvp) -> {
                    try {
                        data.put(kvp.key, kvp.value);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                });

                try {
                    jo.put("data", data);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }

            SendLog(jo.toString());
        }

        sKey = "";
    }

    public static void SendLog(String log) {
        if (sDatagramSocket == null) {
            InitializeSocket();
        }

        DatagramPacket dp = new DatagramPacket(log.getBytes(), log.length(), sInetAddress, sPort);
        try {
            sDatagramSocket.send(dp);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void InitializeSocket() {
        try {
            sInetAddress = InetAddress.getByName(sIP);
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
        try {
            sDatagramSocket = new DatagramSocket(sPort);
        } catch (SocketException e) {
            e.printStackTrace();
        }
    }

    public static String getIP() {
        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && inetAddress instanceof Inet4Address) {
                        return inetAddress.getHostAddress();
                    }
                }
            }
        } catch (SocketException ex) {
            ex.printStackTrace();
        }
        return null;
    }
}
