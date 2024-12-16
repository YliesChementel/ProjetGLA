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
    void shouldReturnIDofBitcoin() throws Exception {
        assertEquals(crypto.getId(), "1");
    }

    @Test
    void shouldSetIDofBitcoin() throws Exception {
        crypto.setId("1");
        assertEquals(crypto.getId(), "1");
    }

    @Test
    void shouldReturnSymbolfBitcoin() throws Exception {
        assertEquals(crypto.getSymbol(), "BTC");
    }

    @Test
    void shouldSetSymbolfBitcoin() throws Exception {
        crypto.setSymbol("BTC");
        assertEquals(crypto.getSymbol(), "BTC");
    }

    @Test
    void shouldReturnNameofBitcoin() throws Exception {
        assertEquals(crypto.getName(), "bitcoin");
    }

    @Test
    void shouldSetNameofBitcoin() throws Exception {
        crypto.setName("bitcoin");
        assertEquals(crypto.getName(), "bitcoin");
    }

    @Test
    void shouldReturnRankofBitcoin() throws Exception {
        assertEquals(crypto.getRank(), 1);
    }

    @Test
    void shouldSetRankofBitcoin() throws Exception {
        crypto.setRank(1);
        assertEquals(crypto.getRank(), 1);
    }

    @Test
    void shouldReturnVolumeofBitcoin() throws Exception {
        assertEquals(crypto.getVolume(), 35539793269.721);
    }

    @Test
    void shouldSetVolumeofBitcoin() throws Exception {
        crypto.setVolume(35539793269.721);
        assertEquals(crypto.getVolume(), 35539793269.721);
    }

    @Test
    void shouldReturnPriceofBitcoin() throws Exception {
        assertEquals(crypto.getPrice(), 98397.5942776494);
    }

    @Test
    void shouldSetPriceofBitcoin() throws Exception {
        crypto.setPrice(98397.5942776494);
        assertEquals(crypto.getPrice(), 98397.5942776494);
    }

}
