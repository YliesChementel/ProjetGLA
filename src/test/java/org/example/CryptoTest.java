package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

import static org.example.Crypto.*;

public class CryptoTest {

    private Crypto crypto;

    @BeforeEach
    public void setup() {
        crypto = new Crypto("1","BTC","bitcoin",1,35539793269.721,98397.5942776494);
    }

    @Test
    void shouldReturnIDofBitcoin(){
        assertEquals("1",crypto.getId());
    }

    @Test
    void shouldSetIDofBitcoin() {
        crypto.setId("1");
        assertEquals("1",crypto.getId());
    }

    @Test
    void shouldReturnSymbolfBitcoin() {
        assertEquals("BTC",crypto.getSymbol());
    }

    @Test
    void shouldSetSymbolfBitcoin() {
        crypto.setSymbol("BTC");
        assertEquals("BTC",crypto.getSymbol());
    }

    @Test
    void shouldReturnNameofBitcoin() {
        assertEquals("bitcoin",crypto.getName());
    }

    @Test
    void shouldSetNameofBitcoin() {
        crypto.setName("bitcoin");
        assertEquals("bitcoin",crypto.getName());
    }

    @Test
    void shouldReturnRankofBitcoin() {
        assertEquals(1,crypto.getRank());
    }

    @Test
    void shouldSetRankofBitcoin() {
        crypto.setRank(1);
        assertEquals(1,crypto.getRank());
    }

    @Test
    void shouldReturnVolumeofBitcoin() {
        assertEquals(35539793269.721,crypto.getVolume());
    }

    @Test
    void shouldSetVolumeofBitcoin() {
        crypto.setVolume(35539793269.721);
        assertEquals(35539793269.721,crypto.getVolume());
    }

    @Test
    void shouldReturnPriceofBitcoin() {
        assertEquals(98397.5942776494,crypto.getPrice());
    }

    @Test
    void shouldSetPriceofBitcoin() {
        crypto.setPrice(98397.5942776494);
        assertEquals(98397.5942776494,crypto.getPrice());
    }

}
