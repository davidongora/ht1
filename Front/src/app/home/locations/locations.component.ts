import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { GoogleMapsModule } from '@angular/google-maps';

interface MarkerInfo {
  lat: number;
  lng: number;
  label: string;
  color: string;
  brand?: string;
}

@Component({
  selector: 'app-locations',
  standalone: true,
  imports: [GoogleMapsModule, CommonModule],
  templateUrl: './locations.component.html',
  styleUrl: './locations.component.css'
})
export class LocationsComponent {
  // Initial center of the map
  center: google.maps.LatLngLiteral = {
    lat: 0.0236,
    lng: 37.9062,
  };

  zoom = 7; // Adjusted zoom level for better view

  // Updated markers with brand information
  markers: MarkerInfo[] = [
    // CMC (New Holland Dealer)
    { lat: -1.286389, lng: 36.817223, label: 'CMC Nairobi', color: 'red', brand: 'New Holland' },
    { lat: -0.2833, lng: 36.0667, label: 'CMC Nakuru', color: 'red', brand: 'New Holland' },
    { lat: 0.01, lng: 37.073, label: 'CMC Nanyuki/Meru', color: 'red', brand: 'New Holland' },
    { lat: 0.52, lng: 35.2777, label: 'CMC Eldoret/Kitale', color: 'red', brand: 'New Holland' },
    { lat: -0.0917, lng: 34.768, label: 'CMC Kisumu', color: 'red', brand: 'New Holland' },
    { lat: -4.0435, lng: 39.6682, label: 'CMC Mombasa', color: 'red', brand: 'New Holland' },

    // Mascor (John Deere)
    { lat: 0.52, lng: 35.2777, label: 'Mascor Eldoret', color: 'green', brand: 'John Deere' },
    { lat: -0.0917, lng: 34.768, label: 'Mascor Kisumu', color: 'green', brand: 'John Deere' },
    { lat: -0.2833, lng: 36.0667, label: 'Mascor Nakuru', color: 'green', brand: 'John Deere' },
    { lat: -1.0921, lng: 35.866, label: 'Mascor Narok', color: 'green', brand: 'John Deere' },

    // FMD (Massey Ferguson)
    { lat: -0.2833, lng: 36.0667, label: 'FMD Nakuru', color: 'blue', brand: 'Massey Ferguson' },
    { lat: 0.52, lng: 35.2777, label: 'FMD Eldoret', color: 'blue', brand: 'Massey Ferguson' },

    // Additional Dealers
    { lat: -1.286389, lng: 36.817223, label: 'CFAO Motors Nairobi', color: 'purple', brand: 'Case IH' },
    { lat: -0.2833, lng: 36.0667, label: 'CFAO Motors Nakuru', color: 'purple', brand: 'Case IH' },
    { lat: -0.0917, lng: 34.768, label: 'CFAO Motors Kisumu', color: 'purple', brand: 'Case IH' },
  ];

  display: google.maps.LatLngLiteral | undefined;

  moveMap(event: google.maps.MapMouseEvent) {
    if (event.latLng) {
      this.center = event.latLng.toJSON();
    }
  }

  move(event: google.maps.MapMouseEvent) {
    if (event.latLng) {
      this.display = event.latLng.toJSON();
    }
  }
}