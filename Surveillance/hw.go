package main

import (
	"fmt"
	"encoding/json"
	"log"
	"net/http"
)

type OID struct {
	Name string
	Oid string
}

type Machine struct {
    Name    string
	IPAddress  string
	IPMask string
	Ports int32
	Community string
	Description string
	MonitoredObjects []OID
}



func main()  {
	resp, err := http.Get("http://localhost:5000/json")
    if err != nil {
        print(err)
    }
	defer resp.Body.Close()
	
	var machineDecoder *json.Decoder = json.NewDecoder(resp.Body)
    if err != nil {
        log.Fatal(err)
	}

	var machineList []Machine

	err = machineDecoder.Decode(&machineList)
    if err != nil {
        log.Fatal(err)
	}
	
	for i, machine := range machineList {
        fmt.Println("Machine", i+1)
		fmt.Println("Machine name:", machine.Name)
		fmt.Println("Machine oid : ", len(machine.MonitoredObjects))
		for j, oid :=range machine.MonitoredObjects{
				fmt.Println("Machine", j+1)
				fmt.Println("oid name ", oid.Name)
				fmt.Println("oid  ", oid.Oid)
			}
			
    }
}