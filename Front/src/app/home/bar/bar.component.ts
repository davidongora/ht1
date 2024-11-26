import { CommonModule } from '@angular/common'; // Import CommonModule
import { Component } from '@angular/core';

@Component({
  selector: 'app-bar',
  standalone: true,
  imports: [CommonModule], // Use CommonModule instead of NgFor and NgIf
  templateUrl: './bar.component.html',
  styleUrls: ['./bar.component.css']
})
export class BarComponent {
  isSidebarCollapsed = false; // state for sidebar collapse

  // Track the currently open menu item (only one can be open at a time)
  currentOpenItemId: number | null = null;

  // Sidebar items
  menuItems = [
    {
      id: 1,
      label: 'MENU',
      isTitle: true
    },
    {
      id: 2,
      label: 'USERS',
      icon: 'ph-users',
      subItems: [
        { id: 3, label: 'View Users', link: '/users', parentId: 2 },
        { id: 4, label: 'Add User', link: '/users/add', parentId: 2 },
        { id: 5, label: 'Manage Users', link: '/users/manage', parentId: 2 }
      ]
    },
    {
      id: 6,
      label: 'INTERNET PLANS',
      icon: 'ph-wifi-high',
      subItems: [
        { id: 7, label: 'View Plans', link: '/plans', parentId: 6 },
        { id: 8, label: 'Add Plan', link: '/plans/add', parentId: 6 },
        { id: 9, label: 'Manage Plans', link: '/plans/manage', parentId: 6 }
      ]
    },
    {
      id: 10,
      label: 'ROUTERS',
      icon: 'ph-router',
      subItems: [
        { id: 11, label: 'View Routers', link: '/routers', parentId: 10 },
        { id: 12, label: 'Add Router', link: '/routers/add', parentId: 10 },
        { id: 13, label: 'Manage Routers', link: '/routers/manage', parentId: 10 }
      ]
    },
    // Add more items as necessary (Networks, Hotspot, Admin, etc.)
  ];

  // Toggle sidebar collapse
  toggleSidebar() {
    this.isSidebarCollapsed = !this.isSidebarCollapsed;
  }

  // Open sub-items for a specific menu item and close others
  toggleSubItems(itemId: number) {
    if (this.currentOpenItemId === itemId) {
      this.currentOpenItemId = null; // Close if already open
    } else {
      this.currentOpenItemId = itemId; // Open and close others
    }
  }

  // Check if sub-items for a menu item are open
  isSubItemsOpen(itemId: number): boolean {
    return this.currentOpenItemId === itemId;
  }
}
