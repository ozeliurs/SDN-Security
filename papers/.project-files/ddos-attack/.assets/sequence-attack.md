```mermaid
sequenceDiagram
    Compromised->>C2: HTTP GET /command
    C2->>Compromised: HTTP "hping3 ... <Victim>"
    loop Flood
        Compromised->> Victim: GET
    end
```