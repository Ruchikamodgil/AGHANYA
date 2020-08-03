import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { UserService } from '../user.service';
declare var google;
@Component({
  selector: 'app-map',
  templateUrl: './map.page.html',
  styleUrls: ['./map.page.scss'],
})
export class MapPage implements OnInit {
map;
@ViewChild('mapElement') mapElement;  
locations = []; 
  constructor(private userService:UserService) { 
    
  }

  ngOnInit() {
  }

  ngAfterViewInit(){  
    this.userService.fetchData().once('value',(res)=>{
      const data:[] = res.val();
      for(let i in data){
        var val :any= data[i]; 
        this.locations.push(['test',val.Lat,val.lon])
      }
      console.log(this.locations)
      this.map = new google.maps.Map(
        this.mapElement.nativeElement,{
          center:{lat:29.972868,lng:76.8879584}, 
          zoom:16
        }
      ) 
  this.markLocation()
    })
    
  }

  markLocation(){ 
    var infowindow = new google.maps.InfoWindow();

var marker, i;
const image = {
  url:'assets/cow.png',
  scaledSize:new google.maps.Size(35,40),
  origin:new google.maps.Point(0,0),
  anchor:new google.maps.Point(15,25)
}

for (i = 0; i < this.locations.length; i++) {   
  marker = new google.maps.Marker({
    position: new google.maps.LatLng(this.locations[i][1], this.locations[i][2]),
    map: this.map,
    icon:image,
    animation: google.maps.Animation.Drop
  });

  google.maps.event.addListener(marker, 'click', ((marker, i)=> {
    return ()=> {
      infowindow.setContent(this.locations[i][0]);
      infowindow.open(this.map, marker);
    }
  })(marker, i));
}
  } 

}
