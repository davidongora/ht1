import { Component, NgModule } from '@angular/core';
import { EndpointsService } from '../../endpoints.service';
import { HttpClient } from '@angular/common/http';
import { NgFor, NgIf } from '@angular/common';
import { GoogleMapsModule } from '@angular/google-maps';


@Component({
  selector: 'app-implements',
  standalone: true,
  imports: [NgFor, NgIf],
  templateUrl: './implements.component.html',
  styleUrl: './implements.component.css'
})
export class ImplementsComponent {
 
tabSelected: 'new' | 'used' = 'new'; // default to 'new' tab
usedTractors: any[] = []; // Array to store used tractors data
brand = ''; // Input value for brand
state = ''; // Input value for state
isLoading = false; // Loading state for API requests


constructor(private endpointsService: EndpointsService, private http: HttpClient) {}




ngOnInit(): void {
  //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
  //Add 'implements OnInit' to the class.
  this.searchUsedTractor()
  this.GetUsedTractors()
  console.log(this.usedTractors)
  
}
searchUsedTractor() {
  // Logic for searching used tractors
  const url = this.endpointsService.endpoint.SEARCH_USED_TRACTORS;
  const params = {
    brand: this.brand,
    state: this.state,
  };

  this.isLoading = true;
  this.http.get(url, { params }).subscribe({
    next: (response: any) => {
      this.usedTractors = response.data[0]; // Assuming API returns `data` key
      this.isLoading = false;
    },
    error: (error) => {
      console.error('Error fetching used tractors:', error);
      this.isLoading = false;
    },
  });
}

GetUsedTractors() {
  // Logic for retrieving all used tractors
  const url = this.endpointsService.endpoint.GET_USED_TRACTORS;

  this.isLoading = true;
  this.http.get(url).subscribe({
    next: (response: any) => {
      this.usedTractors = response.tractors; // Assuming API returns `data` key
      this.isLoading = false;
    },
    error: (error) => {
      console.error('Error fetching used tractors:', error);
      this.isLoading = false;
    },
  });
}

toggleFavorite(tractor: any): void {
  tractor.Favorite = !tractor.Favorite; // Toggle favorite status
  // Optionally, send an API request to save the favourite state
  console.log(`Tractor ${tractor.TractorID} favorite status: ${tractor.Favorite}`);
}

}
