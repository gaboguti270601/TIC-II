#include "lwip/sockets.h"
#include "esp_log.h"
#include "esp_wifi.h"

#define SERVER_IP           "10.42.0.1"
#define SERVER_PORT_TCP     1234

extern const char* TAG;

void socket_tcp() {
    struct sockaddr_in server_addr;

    // Obtener la dirección MAC del ESP32
    uint8_t mac[6];
    esp_wifi_get_mac(WIFI_IF_STA, mac);

    // Crear una variable para el ID_Device utilizando los primeros 2 bytes de la dirección MAC
    char id_device[5];
    snprintf(id_device, sizeof(id_device), "%02x%02x", mac[0], mac[1]);


    // Crear una variable para el mensaje
    const char *mensaje = "Hola Mundo";

    // Calcular el largo del mensaje
    int mensaje_length = strlen(mensaje);

    // Crear una variable para el Transport_layer
    const char *Transport_layer = "0";

    // Crear una variable para el ID_Protocol
    const char *ID_Protocol = "7";

    // Crear una variable para la dirección MAC
    char mac_str[18];  // 6 bytes en formato hexadecimal y 5 guiones
    snprintf(mac_str, sizeof(mac_str), "%02x:%02x:%02x:%02x:%02x:%02x", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

    // Crear un formato de mensaje que incluya el ID_Device, la dirección MAC, el Transport_layer, el ID_Protocol, el largo del mensaje y el mensaje
    char message[128];
    snprintf(message, sizeof(message), "%s - %s - %s - %s - %d - %s", id_device, mac_str, Transport_layer, ID_Protocol, mensaje_length, mensaje);

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT_TCP);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr.s_addr);

    // Crear un socket
    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock < 0) {
        ESP_LOGE(TAG, "Error al crear el socket");
        return;
    }

    // Conectar al servidor
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) != 0) {
        ESP_LOGE(TAG, "Error al conectar");
        close(sock);
        return;
    }

    // Enviar el mensaje que incluye el ID_Device, la dirección MAC, el Transport_layer, el ID_Protocol, el largo del mensaje y el mensaje al servidor
    send(sock, message, strlen(message), 0);

    // Recibir respuesta
    char rx_buffer[128];
    int rx_len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
    if (rx_len < 0) {
        ESP_LOGE(TAG, "Error al recibir datos");
        return;
    }
    rx_buffer[rx_len] = '\0';  // Asegurar que el buffer esté terminado con null para imprimir correctamente
    ESP_LOGI(TAG, "Datos recibidos: %s", rx_buffer);

    // Cerrar el socket
    close(sock);
}
