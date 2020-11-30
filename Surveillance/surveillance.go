package main

import (
	"fmt"
	"encoding/json"
	"log"
	"net/http"
	g "github.com/gosnmp/gosnmp"
	"os"
	"time"
	client "github.com/influxdata/influxdb1-client"
	// "math/big"
	// "math/rand"
	"net/url"
	// "strconv"
	// "reflect"
	)

type OID struct {
	Name string
	Oid string
}

type Machine struct {
    Name    string
	IPAddress  string
	IPMask string
	Ports uint16
	Community string
	Description string
	MonitoredObjects []OID
}

func main()  {
	ticker := time.NewTicker(30 * time.Second)

	for _ = range ticker.C {

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
		
		for _, machine := range machineList {
			// fmt.Println("Machine name:", i+1)

			
			params := &g.GoSNMP{
				Target:   machine.IPAddress,
				Port:      machine.Ports,
				Community: machine.Community,
				Version:   g.Version2c,
				Timeout:       time.Duration(1) * time.Second,
				Logger:    log.New(os.Stdout, "", 0),
			}
			err := params.Connect()
			if err != nil {
				log.Fatalf("Connect() err: %v", err)
			}
			defer params.Conn.Close()

			var oids = make([]string, len(machine.MonitoredObjects))
			for k := 0; k < len(machine.MonitoredObjects); k++ {
				oids[k]=machine.MonitoredObjects[k].Oid
			}
			// oids := []string{"1.3.6.1.2.1.1.1.0","1.3.6.1.2.1.1.4.0","1.3.6.1.2.1.1.5.0","1.3.6.1.2.1.1.6.0"}

			result, err2 := params.Get(oids) // Get() accepts up to g.MAX_OIDS
			if err2 != nil {
				log.Fatalf("Get() err: %v", err2)
			}

			host, err := url.Parse(fmt.Sprintf("http://%s:%d", "localhost", 8086))
			if err != nil {
				log.Fatal(err)
			}
			con, err := client.NewClient(client.Config{URL: *host})
			if err != nil {
				log.Fatal(err)
			}
			var pts = make([]client.Point, 10000)

			for i, variable := range result.Variables {
				if variable.Type == g.OctetString {
					var value = string(variable.Value.([]byte))
					pts[i] = client.Point{
						Measurement: variable.Name,
						Tags: map[string]string{
							"host": machine.Name,
						},
						Fields: map[string]interface{}{
							"value": value,
						},
						Time:time.Now(),
						Precision: "n",
					}
				}else {
					var value = g.ToBigInt(variable.Value).Int64()
					// var value = variable.Value
					// fmt.Println(reflect.TypeOf(value).String())
					pts[i] = client.Point{
						Measurement: variable.Name,
						Tags: map[string]string{
							"host": machine.Name,
						},
						Fields: map[string]interface{}{
							"value": value,
						},
						Time:time.Now(),
						Precision: "n",
					}
				}
				// switch variable.Type {
				// case g.OctetString:
				// 	value = string(variable.Value.([]byte))
				// default:
				// 	value = g.ToBigInt(variable.Value)
				// }
		
			}

			bps := client.BatchPoints{
				Points:          pts,
				Database:        "sampledb",
				RetentionPolicy: "autogen",
			}

			_, err = con.Write(bps)

			if err != nil {
				log.Fatal(err)
			}
		}
	}
}