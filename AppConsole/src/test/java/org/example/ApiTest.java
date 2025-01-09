package org.example;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.sql.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.*;
import java.util.logging.Logger;

import static org.example.CryptoDataBase.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class ApiTest {

    Api api;

    @BeforeEach
    void setup() {
        Logger logger = Logger.getLogger(Api.class.getName());
        api = new Api(logger);
    }

    @Test
    void shouldReturnApiRequest() {
        String url = "https://api.example.com/data";
        HttpRequest request = api.takeApiRequest(url);
        assertNotNull(request);
        assertEquals(URI.create(url), request.uri());
        assertTrue(request.headers().map().containsKey("Accept"));
    }

    @Test
    void shouldReturnJsonRequest() throws IOException, InterruptedException {
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
    void shouldReturnNullWhenStatus400() throws IOException, InterruptedException {
        HttpClient mockClient = mock(HttpClient.class);
        HttpRequest mockRequest = mock(HttpRequest.class);
        HttpResponse<String> mockResponse = mock(HttpResponse.class);

        String jsonResponse = "{}";
        when(mockResponse.body()).thenReturn(jsonResponse);
        when(mockResponse.statusCode()).thenReturn(400);
        when(mockClient.send(mockRequest, HttpResponse.BodyHandlers.ofString())).thenReturn(mockResponse);

        JSONArray assets = api.takeJsonRequest(mockRequest, mockClient);

        assertNull(assets);
    }

    @Test
    void shouldReturnNullWhenStatus500() throws IOException, InterruptedException {
        HttpClient mockClient = mock(HttpClient.class);
        HttpRequest mockRequest = mock(HttpRequest.class);
        HttpResponse<String> mockResponse = mock(HttpResponse.class);

        String jsonResponse = "{}";
        when(mockResponse.body()).thenReturn(jsonResponse);
        when(mockResponse.statusCode()).thenReturn(500);
        when(mockClient.send(mockRequest, HttpResponse.BodyHandlers.ofString())).thenReturn(mockResponse);

        JSONArray assets = api.takeJsonRequest(mockRequest, mockClient);

        assertNull(assets);
    }

    @Test
    void shouldReturnNullWhenStatusIsOther() throws IOException, InterruptedException {
        HttpClient mockClient = mock(HttpClient.class);
        HttpRequest mockRequest = mock(HttpRequest.class);
        HttpResponse<String> mockResponse = mock(HttpResponse.class);

        String jsonResponse = "{}";
        when(mockResponse.body()).thenReturn(jsonResponse);
        when(mockResponse.statusCode()).thenReturn(250);
        when(mockClient.send(mockRequest, HttpResponse.BodyHandlers.ofString())).thenReturn(mockResponse);

        JSONArray assets = api.takeJsonRequest(mockRequest, mockClient);

        assertNull(assets);
    }

    @Test
    void shouldReturnTime() {
        String currentTime = api.takeTime();
        assertNotNull(currentTime);
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        LocalDateTime now = LocalDateTime.now();
        assertArrayEquals(dtf.format(now).toCharArray(), currentTime.toCharArray());
    }

    @Test
    void shouldBreakWhenAssetNull() throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:sqlite::memory:");
        HttpClient mockClient = mock(HttpClient.class);
        HttpRequest mockRequest = mock(HttpRequest.class);
        HttpResponse<String> mockResponse = mock(HttpResponse.class);

        String jsonResponse = "{}";
        when(mockResponse.body()).thenReturn(jsonResponse);
        when(mockResponse.statusCode()).thenReturn(400);
        when(mockClient.send(mockRequest, HttpResponse.BodyHandlers.ofString())).thenReturn(mockResponse);

        Api apiSpy = spy(api);

        apiSpy.apiRun(conn, mockClient, mockRequest,1);

        // Vérifier que la boucle while s'est terminée sans exécuter la suite du code
        verify(apiSpy, times(1)).takeJsonRequest(any(HttpRequest.class), any(HttpClient.class));  // Vérifier que takeJsonRequest a bien été appelé une fois
    }

    @Test
    void shouldInteractWithDatabase() throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:sqlite::memory:"); // In-memory database
        createCrypto(conn);
        createCryptoData(conn);

        HttpClient mockClient = mock(HttpClient.class);
        HttpRequest mockRequest = mock(HttpRequest.class);
        HttpResponse<String> mockResponse = mock(HttpResponse.class);

        String jsonResponse = "{ \"data\": [ { \"id\": \"1\", \"rank\": \"1\", \"symbol\": \"BTC\", \"name\": \"Bitcoin\", \"volumeUsd24Hr\": 1000, \"priceUsd\": 50000 } ] }";
        when(mockResponse.body()).thenReturn(jsonResponse);
        when(mockResponse.statusCode()).thenReturn(200);
        when(mockClient.send(mockRequest, HttpResponse.BodyHandlers.ofString())).thenReturn(mockResponse);

        // Exécution de apiRun avec un timeout de 1 seconde
        ExecutorService executor = java.util.concurrent.Executors.newSingleThreadExecutor();
        Callable<Void> task = () -> {
            api.apiRun(conn, mockClient, mockRequest, 1);  // Appel à la méthode apiRun
            return null;  // Retourne null, car l'API n'a pas de valeur de retour
        };

        Future<Void> future = executor.submit(task);
        try {
            future.get(1, TimeUnit.SECONDS);  // Attente de la tâche pendant 1 seconde
        } catch (java.util.concurrent.TimeoutException e) {
            // Si la tâche dépasse 1 seconde, elle sera annulée
            future.cancel(true);  // Annule la tâche si elle prend trop de temps
            System.out.println("Timeout reached, task was cancelled.");
        } catch (ExecutionException | InterruptedException e) {
            // Gestion des exceptions de l'exécution de la tâche
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }


        // Vérification de l'insertion dans la base de données
        Statement selectStatement = conn.createStatement();
        ResultSet resultSet = selectStatement.executeQuery("SELECT * FROM CryptoData WHERE id = '1'");

        // Vérification des données insérées
        assertTrue(resultSet.next());
        assertEquals(1, resultSet.getInt("Rank"));
        assertEquals(50000, resultSet.getDouble("Price"));
        assertEquals(1000, resultSet.getDouble("Volume"));
    }

}
