#include "Conexion_wifi.c"
#include "Cliente_TCP.c"
#include "Cliente_UDP.c"

void app_main(void) {
    nvs_init();
    wifi_init_sta(WIFI_SSID, WIFI_PASSWORD);
    ESP_LOGI(TAG, "Conectado a WiFi!\n");

    #define Transport_layer 0

    if (Transport_layer == 0) {
        socket_tcp();
    } else if (Transport_layer == 1) {
        xTaskCreate(udp_client_task, "udp_client_task", 4096, NULL, 5, NULL);
    }
}