package org.example;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class ApiTest {

    // Test the takeApiRequest() method
    @Test
    public void shouldReturnApiRequest() {
        String url = "https://api.example.com/data";
        HttpRequest request = Api.takeApiRequest(url);
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

        JSONArray assets = Api.takeJsonRequest(mockRequest, mockClient);

        assertNotNull(assets);
        assertEquals(1, assets.length());
        JSONObject asset = assets.getJSONObject(0);
        assertEquals("BTC", asset.getString("symbol"));
        assertEquals(50000, asset.getDouble("priceUsd"));
    }

    @Test
    public void shouldReturnTime() {
        String currentTime = Api.takeTime();
        assertNotNull(currentTime);
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        LocalDateTime now = LocalDateTime.now();
        assertArrayEquals(dtf.format(now).toCharArray(), currentTime.toCharArray());
    }

    @Test
    public void shouldReturnJsonResponse() throws IOException, InterruptedException {
        HttpClient mockClient = mock(HttpClient.class);
        HttpRequest mockRequest = mock(HttpRequest.class);
        HttpResponse<String> mockResponse = mock(HttpResponse.class);

    }

    @Test
    public void shouldReturnInstance(){
        Api api = new Api();
        assertNotNull(api);
    }
}
