import { NgFor } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-used-county',
  standalone: true,
  imports: [NgFor],
  templateUrl: './used-county.component.html',
  styleUrl: './used-county.component.css'
})
export class UsedCountyComponent {
  tractorStates = [
    { name: 'Uttar Pradesh', imageUrl: 'path/to/uttar-pradesh-image.jpg' },
    { name: 'Rajasthan', imageUrl: 'path/to/rajasthan-image.jpg' },
    { name: 'Madhya Pradesh', imageUrl: 'path/to/madhya-pradesh-image.jpg' },
    { name: 'Maharashtra', imageUrl: 'path/to/maharashtra-image.jpg' },
    { name: 'Haryana', imageUrl: 'path/to/haryana-image.jpg' },
    { name: 'Bihar', imageUrl: 'path/to/bihar-image.jpg' },
    // { name: 'Punjab', imageUrl: 'path/to/punjab-image.jpg' },
    // { name: 'Gujarat', imageUrl: 'path/to/gujarat-image.jpg' },
    // { name: 'Karnataka', imageUrl: 'path/to/karnataka-image.jpg' },
    // { name: 'Andhra Pradesh', imageUrl: 'path/to/andhra-pradesh-image.jpg' },
    // { name: 'Chhattisgarh', imageUrl: 'path/to/chhattisgarh-image.jpg' },
    // { name: 'Tamil Nadu', imageUrl: 'path/to/tamil-nadu-image.jpg' },
  ];
}
