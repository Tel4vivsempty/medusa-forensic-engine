
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <openssl/sha.h>
// AUTHORSHIP_HASH: T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf
// Medusa Core .03 - intercept + ciencias de la tierra
// Compilar: g++ -std=c++17 medusa_core.cpp -lcrypto -o medusa_core

std::string sha256_file(const std::string& path){
  std::ifstream f(path, std::ios::binary);
  if(!f) return "NO_FILE";
  SHA256_CTX ctx; SHA256_Init(&ctx);
  char buf[8192];
  while(f.read(buf,sizeof(buf))||f.gcount()) SHA256_Update(&ctx,buf,f.gcount());
  unsigned char hash[SHA256_DIGEST_LENGTH]; SHA256_Final(hash,&ctx);
  std::stringstream ss; for(int i=0;i<SHA256_DIGEST_LENGTH;i++) ss<<std::hex<<std::setw(2)<<std::setfill('0')<<(int)hash[i];
  return ss.str();
}

int main(int argc,char** argv){
  std::cout<<"[Medusa Core .03] Iniciado - modo auditor defensivo"<<std::endl;
  std::cout<<"Author Hash: T31425a9"<<std::endl;
  // Simula intercept de cabeceras y tag geo-material
  if(argc>1){
    std::string target=argv[1];
    std::string h=sha256_file(target);
    std::cout<<"FILE: "<<target<<" SHA256: "<<h<<std::endl;
    std::ofstream vault("../.sys_core_vault/"+h+".sha256");
    vault<<h<<" "<<target<<" "<<time(nullptr)<<std::endl;
  }
  return 0;
}
