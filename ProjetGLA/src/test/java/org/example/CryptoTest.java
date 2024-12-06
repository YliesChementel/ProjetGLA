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
        assertEquals(crypto, "Sacha");
    }

}
