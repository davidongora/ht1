import { Component, NgModule } from '@angular/core';
import { EndpointsService } from '../../endpoints.service';
import { HttpClient } from '@angular/common/http';
import { NgFor, NgIf } from '@angular/common';
import { GoogleMapsModule } from '@angular/google-maps';
import { NgModel } from '@angular/forms';

interface UsedTractor {
  TractorID?: number;
  brand: string;
  Location: string;
  HpPower: number;
  HoursUsed: number;
  Price: number;
  Description: string;
  Image: string;
  Favorite?: boolean;
}

@Component({
  selector: 'app-tractors',
  standalone: true,
  imports: [NgIf, NgFor, GoogleMapsModule ],
  templateUrl: './tractors.component.html',
  styleUrl: './tractors.component.css'
})
export class TractorsComponent {

  tabSelected: 'new' | 'used' = 'used';
  usedTractors: UsedTractor[] = [];
  brand = '';
  state = '';
  isLoading = false;

  // Message Modal Properties
  isMessageModalOpen = false;
  selectedTractor: UsedTractor | null = null;
  messageSubject = '';
  messageBody = '';

  constructor(
    private endpointsService: EndpointsService, 
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.searchUsedTractor();
    this.GetUsedTractors();
  }

  searchUsedTractor() {
    const url = this.endpointsService.endpoint.SEARCH_USED_TRACTORS;
    const params = {
      brand: this.brand,
      state: this.state,
    };

    this.isLoading = true;
    this.http.get(url, { params }).subscribe({
      next: (response: any) => {
        this.usedTractors = response.data[0];
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error fetching used tractors:', error);
        this.isLoading = false;
      },
    });
  }

  GetUsedTractors() {
    const url = this.endpointsService.endpoint.GET_USED_TRACTORS;

    this.isLoading = true;
    this.http.get(url).subscribe({
      next: (response: any) => {
        this.usedTractors = response.tractors;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error fetching used tractors:', error);
        this.isLoading = false;
      },
    });
  }

  toggleFavorite(tractor: UsedTractor): void {
    tractor.Favorite = !tractor.Favorite;
    console.log(`Tractor ${tractor.TractorID} favorite status: ${tractor.Favorite}`);
  }

  openMessageModal(tractor: UsedTractor) {
    this.selectedTractor = tractor;
    this.isMessageModalOpen = true;
    
    // Set default subject
    this.messageSubject = `Inquiry about ${tractor.brand} Tractor`;
    this.messageBody = '';
  }

  closeMessageModal() {
    this.isMessageModalOpen = false;
    this.selectedTractor = null;
  }

  sendMessage() {
    if (!this.selectedTractor) return;

    // Implement your messaging service logic here
    console.log('Sending message:', {
      tractorId: this.selectedTractor.TractorID,
      subject: this.messageSubject,
      body: this.messageBody
    });

    // Example: You might want to call a service method to send the message
    // this.messagingService.sendMessage(...)

    // Show success notification
    alert('Message sent successfully!');

    // Close the modal
    this.closeMessageModal();
  }
}