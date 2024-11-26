import { Component, NgModule } from '@angular/core';
import {HeaderComponent} from '../header/header.component'
import { ButtonsComponent } from "../buttons/buttons.component";
import { CommonModule, NgIf } from '@angular/common';
import { EndpointsService } from '../../endpoints.service';

interface Tractor {
  id: string;
  brand: string;
  state: string;
  price: number;
  description?: string;
}

@Component({
  selector: 'app-info',
  standalone: true,
  imports: [HeaderComponent, ButtonsComponent, CommonModule],
  templateUrl: './info.component.html',
  styleUrl: './info.component.css'
})
export class InfoComponent {
  tabSelected: 'new' | 'used' = 'new'; // default to 'new' tab

  tractors: any[] = []; // To store fetched tractors
  searchCriteria: { brand: string; state: string } = { brand: '', state: '' };
 // Modal control
  isModalOpen = false;
  modalTitle = '';
  modalMessage = '';
  selectedTractor: Tractor | null = null;

  constructor(private endpointsService: EndpointsService) {}


  sliderImages: string[] = [
    'https://ht-mobileassets.s3.amazonaws.com/tractorModels/DI-35-removebg-preview.png',
    'https://s3-us-west-2.amazonaws.com/ht-mobileassets/ti_massey_ferguson_tractor_mf5710.png',
    'https://ht-mobileassets.s3.amazonaws.com/tractorModels/Yanmar.jpg',
    'https://ht-mobileassets.s3.amazonaws.com/tractorModels/Case_IH_JX90.png',
  ];
  currentSlide: number = 0;

  nextSlide(): void {
    this.currentSlide = (this.currentSlide + 1) % this.sliderImages.length;
  }

  prevSlide(): void {
    this.currentSlide =
      (this.currentSlide - 1 + this.sliderImages.length) % this.sliderImages.length;
  }

  searchUsedTractor() {
    // Validate search criteria
    if (!this.searchCriteria.brand || !this.searchCriteria.state) {
      this.openModal('Search Error', 'Please fill in both Brand and State');
      return;
    }

    const params = {
      brand: this.searchCriteria.brand,
      state: this.searchCriteria.state
    };

    this.endpointsService.http
      .get<Tractor[]>(this.endpointsService.endpoint.SEARCH_USED_TRACTORS, { params })
      .subscribe({
        next: (data) => {
          if (data.length > 0) {
            this.tractors = data;
            this.openModal('Search Results', `Found ${data.length} tractors matching your criteria`);
          } else {
            this.openModal('No Results', 'No tractors found matching your search criteria');
          }
        },
        error: (err) => {
          this.openModal('Search Error', 'Failed to search tractors. Please try again.');
          console.error('Error fetching used tractors:', err);
        }
      });
  }

  // Method to open modal
  openModal(title: string, message: string, tractor?: Tractor) {
    this.isModalOpen = true;
    this.modalTitle = title;
    this.modalMessage = message;
    this.selectedTractor = tractor || null;
  }

  // Method to close modal
  closeModal() {
    this.isModalOpen = false;
  }

  // Method to view tractor details
  viewTractorDetails(tractor: Tractor) {
    this.openModal('Tractor Details', '', tractor);
  }


  GetUsedTractors() {
    this.endpointsService.http
      .get(this.endpointsService.endpoint.GET_USED_TRACTORS)
      .subscribe({
        next: (data: any) => {
          this.tractors = data; // Assume the API returns a list of tractors
          console.log('All Used Tractors:', this.tractors);
        },
        error: (err) => {
          console.error('Error fetching used tractors:', err);
        }
      });
  }

}
