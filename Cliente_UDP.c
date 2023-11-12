#include "lwip/sockets.h"
#include "lwip/dns.h"
#include "lwip/netdb.h"
#include "esp_log.h"
#include "esp_wifi.h"

#define SERVER_IP           "10.42.0.1"
#define SERVER_PORT_UDP     1235

extern const char* TAG;

void udp_client_task(void *pvParameters) {
    struct sockaddr_in server_addr;

    while (1) {
        int sock = socket(AF_INET, SOCK_DGRAM, 0);
        if (sock < 0) {
            ESP_LOGE(TAG, "Error al crear el socket UDP");
            vTaskDelay(1000 / portTICK_PERIOD_MS);
            continue;
        }

        // Obtener la dirección MAC del ESP32
        uint8_t mac[6];
        esp_wifi_get_mac(WIFI_IF_STA, mac);

        // Crear una variable para la dirección MAC
        char mac_str[18];  // 6 bytes en formato hexadecimal y 5 guiones
        snprintf(mac_str, sizeof(mac_str), "%02x:%02x:%02x:%02x:%02x:%02x", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

        // Crear una variable para el mensaje
        const char *mensaje = "Hola Mundo";

        // Calcular el largo del mensaje
        int mensaje_length = strlen(mensaje);

        // Crear una variable para el ID_Device
        const char *ID_Device = "03";

        // Crear una variable para el Transport_layer
        const char *Transport_layer = "1";

        // Crear una variable para el ID_Protocol
        const char *ID_Protocol = "7";

        // Crear un formato de mensaje que incluya el ID_Device, la dirección MAC, el Transport_layer, el ID_Protocol, el largo del mensaje y el mensaje
        char message[128];
        snprintf(message, sizeof(message), "%s - %s - %s - %s - %d - %s", ID_Device, mac_str, Transport_layer, ID_Protocol, mensaje_length, mensaje);

        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(SERVER_PORT_UDP);
        inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr.s_addr);

        // Enviar datos al servidor UDP
        int err = sendto(sock, message, strlen(message), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
        if (err < 0) {
            ESP_LOGE(TAG, "Error al enviar datos");
        }

        // Cerrar el socket UDP
        close(sock);

        vTaskDelay(5000 / portTICK_PERIOD_MS); // Envía datos cada 5 segundos
    }
}