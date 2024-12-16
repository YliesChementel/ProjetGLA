package org.example;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.logging.Logger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class ApiTest {

    Api api;

    @BeforeEach
    public void setup() {
        Logger logger = Logger.getLogger(Api.class.getName());
        api = new Api(logger);
    }

    @Test
    public void shouldReturnApiRequest() {
        String url = "https://api.example.com/data";
        HttpRequest request = api.takeApiRequest(url);
        assertNotNull(request);
        assertEquals(URI.create(url), request.uri());
        assertTrue(request.headers().map().containsKey("Accept"));
    }

    @Test
    public void shouldReturnJsonRequest() throws IOException, InterruptedException {
        HttpClient mockClient = mock(HttpClient.class);
        HttpRequest mockRequest = mock(HttpRequest.class);
        HttpResponse<String> mockResponse = mock(HttpResponse.class);

        String jsonResponse = "{ \"data\": [{ \"id\": \"1\", \"symbol\": \"BTC\", \"name\": \"Bitcoin\", \"rank\": 1, \"volumeUsd24Hr\": 1000, \"priceUsd\": 50000 }] }";
        when(mockResponse.body()).thenReturn(jsonResponse);
        when(mockResponse.statusCode()).thenReturn(200);
        when(mockClient.send(mockRequest, HttpResponse.BodyHandlers.ofString())).thenReturn(mockResponse);

        JSONArray assets = api.takeJsonRequest(mockRequest, mockClient);

        assertNotNull(assets);
        assertEquals(1, assets.length());
        JSONObject asset = assets.getJSONObject(0);
        assertEquals("BTC", asset.getString("symbol"));
        assertEquals(50000, asset.getDouble("priceUsd"));
    }

    @Test
    public void shouldReturnTime() {
        String currentTime = api.takeTime();
        assertNotNull(currentTime);
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        LocalDateTime now = LocalDateTime.now();
        assertArrayEquals(dtf.format(now).toCharArray(), currentTime.toCharArray());
    }



    @Test
    public void testTakeTime() {
        String result = api.takeTime();

        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        String expectedFormat = LocalDateTime.now().format(dtf);

        assertTrue(result.matches("\\d{4}/\\d{2}/\\d{2} \\d{2}:\\d{2}:\\d{2}"));

        assertEquals(expectedFormat.substring(0, 10), result.substring(0, 10));
        assertEquals(expectedFormat.substring(11, 19), result.substring(11, 19));
    }
}
