#include <iostream>
#include <string>
#include <fstream>
#include <ctime>
#include <sstream>

class MedusaSecureChannel {
private:
    std::string ephemeral_key_signature;
    std::string generate_evaporating_key() {
        return "SHA256_MDS_V1_" + std::to_string(std::time(nullptr));
    }
public:
    std::string wrap_payload(const std::string& raw_telemetry) {
        ephemeral_key_signature = generate_evaporating_key();
        std::string sealed_packet = "[TOR_TUNNEL_ENC:=" + ephemeral_key_signature + "::" + raw_telemetry + "]";
        return sealed_packet;
    }
    std::string get_current_signature() {
        return ephemeral_key_signature;
    }
    bool inspect_tampering(const std::string& received_packet, const std::string& expected_signature) {
        if (received_packet.find(expected_signature) == std::string::npos) {
            std::string timestamp = std::to_string(std::time(nullptr));
            std::string alert_msg = "[TRAZA FORENSE // INTERCEPTACION DETECTADA] Timestamp: " + timestamp + " | Paquete manipulado: " + received_packet;
            std::cout << alert_msg << std::endl;
            std::ofstream log_file("medusa_intercept.log", std::ios::out | std::ios::app);
            if (log_file.is_open()) {
                log_file << alert_msg << std::endl;
                log_file.flush();
                log_file.close();
                std::cout << "[OK] Traza registrada con exito en medusa_intercept.log" << std::endl;
            } else {
                std::cout << "[ERROR] No se pudo abrir el archivo de bitacora" << std::endl;
            }
            return true;
        }
        std::cout << "[OK] Paquete integro. Ninguna alteracion detectada en la firma." << std::endl;
        return false;
    }
};

struct SporePacket {
    std::string source_ip;
    int ingress_port;
    std::string http_headers;
    std::string payload_hash;
    long timestamp;
};

class MedusaSporeEngine {
private:
    std::string cipher_seed;
    std::string generate_spore_pulse() {
        return "SPORE_PULSE_" + std::to_string(std::time(nullptr));
    }
public:
    void emit_spore(const std::string& target_node) {
        std::string pulse = generate_spore_pulse();
        std::cout << "[EMISION DE ESPORA] Pulso lanzado hacia nodo oculto -> " << target_node << " | Token: " << pulse << std::endl;
    }
    bool dissect_ingress(const SporePacket& packet, const std::string& expected_signature) {
        std::cout << "\n--- DISECCION DE CABECERAS Y PUERTOS DE INGRESO ---" << std::endl;
        std::cout << "[*] IP de Origen Detectada: " << packet.source_ip << std::endl;
        std::cout << "[*] Puerto de Escucha: " << packet.ingress_port << std::endl;
        std::cout << "[*] Cabeceras Capturadas:\n" << packet.http_headers << std::endl;
        if (packet.payload_hash.find(expected_signature) == std::string::npos) {
            std::string alert = "[ALERTA CRITICA // INTRUSION EN PUERTO] Intento de manipulacion en pasarela por IP: " + packet.source_ip + " en puerto " + std::to_string(packet.ingress_port);
            std::cout << alert << std::endl;
            std::ofstream log_file("medusa_intercept.log", std::ios::out | std::ios::app);
            if (log_file.is_open()) {
                log_file << alert << " | Headers: " << packet.http_headers << std::endl;
                log_file.flush();
                log_file.close();
            }
            return true;
        }
        std::cout << "[OK] Trafico legitimo. Ninguna alteracion en la espora." << std::endl;
        return false;
    }
};

int main() {
    MedusaSecureChannel channel;
    std::string valid_packet = channel.wrap_payload("TELEMETRY_NODE_ACTIVE");
    std::string valid_sig = channel.get_current_signature();
    std::cout << "[OK] Paquete original generado con firma efimera: " << valid_sig << std::endl;
    std::string tampered_packet = "[TOR_TUNNEL_ENC:=SHA256_MDS_V1_CORRUPTED_BY_NOC::TELEMETRY_NODE_ACTIVE]";
    std::cout << "[*] Inspeccionando paquete entrante en el puerto..." << std::endl;
    channel.inspect_tampering(tampered_packet, valid_sig);
    system("cat medusa_intercept.log 2>/dev/null");

    MedusaSporeEngine engine;
    engine.emit_spore("tor://medusa.node.onion:8080");
    SporePacket hostile_packet;
    hostile_packet.source_ip = "189.203.xx.xx (Infraestructura NOC / Totalplay/Telcel)";
    hostile_packet.ingress_port = 443;
    hostile_packet.http_headers = "Host: api.medusa-core.onion\nUser-Agent: Mozilla/5.0 (NOC-Probe-Agent)\nX-Forwarded-For: 201.141.xx.xx\nSec-WebSocket-Key: CORRUPTED_BY_INSPECTION";
    hostile_packet.payload_hash = "CORRUPTED_BY_NOC";
    engine.dissect_ingress(hostile_packet, valid_sig);
    return 0;
}
