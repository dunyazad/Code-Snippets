package com.imc;

import java.util.HashMap;

public class EventRegulator {
    private static EventRegulator sinstance = null;

    private static HashMap<String, EventRegulatorElement> sEventRegulatorElements;
    private EventRegulator() {
        sEventRegulatorElements = new HashMap<>();
    }

    public static long Event(String key, long eventPerSecond) {
        if(sinstance == null) {
            sinstance = new EventRegulator();
        }

        if(sEventRegulatorElements.containsKey(key) == false) {
            sEventRegulatorElements.put(key, new EventRegulatorElement(eventPerSecond));
        }

        return sEventRegulatorElements.get(key).Event(eventPerSecond);
    }
}
