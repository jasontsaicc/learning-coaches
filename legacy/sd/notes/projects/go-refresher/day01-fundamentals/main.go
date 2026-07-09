package main

import "fmt"

// Contact represents a phonebook entry
type Contact struct {
	Name      string
	Phone     string
	Emergency bool
}

// Display returns a formatted string of the contact (value receiver — read only)
func (c Contact) Display() string {
	return c.Name + " - " + c.Phone
}

// UpdatePhone changes the contact's phone number (pointer receiver — modifies original)
func (c *Contact) UpdatePhone(newPhone string) {
	c.Phone = newPhone
}

// ToggleEmergency flips the Emergency field (pointer receiver — modifies original)
func (c *Contact) ToggleEmergency() {
	c.Emergency = !c.Emergency
}

// FindContact searches for a contact by name
func FindContact(name string, phonebook []Contact) (Contact, error) {
	for _, c := range phonebook {
		if c.Name == name {
			return c, nil
		}
	}
	return Contact{}, fmt.Errorf("contact %s not found", name)
}

// AddContact adds a new contact to the phonebook, returns error if name already exists
func AddContact(name string, phone string, phonebook []Contact) ([]Contact, error) {
	_, err := FindContact(name, phonebook)
	if err == nil {
		return phonebook, fmt.Errorf("contact %s already exists", name)
	}
	phonebook = append(phonebook, Contact{Name:name, Phone:phone})
		return phonebook, nil
}

// ListContacts prints all contacts in the phonebook
func ListContacts(phonebook []Contact) {
	fmt.Println("=== Phonebook ===")
	for _, c := range phonebook {
		fmt.Println(c.Display())
	}
	fmt.Println("=================")
}

// DeleteContact removes a contact by name, returns error if not found
func DeleteContact(name string, phonebook []Contact) ([]Contact, error) {
	for i, c :=range phonebook {
		if c.Name == name {
			phonebook = append(phonebook[:i], phonebook[i+1:]...)
			return phonebook, nil
		}
	}
	return phonebook, fmt.Errorf("contact %s not found", name)}

func main() {
	phonebook := []Contact{
		{Name: "Alice", Phone: "0912345678", Emergency: true},
		{Name: "Bob", Phone: "0922222222", Emergency: false},
	}

	fmt.Println("--- Initial ---")
	ListContacts(phonebook)

	// Test: Add new contact
	var err error
	phonebook, err = AddContact("Charlie", "0933333333", phonebook)
	if err != nil {
		fmt.Println("Add error:", err)
	}

	// Test: Add duplicate contact
	phonebook, err = AddContact("Alice", "0999999999", phonebook)
	if err != nil {
		fmt.Println("Add error:", err)
	}

	fmt.Println("--- After Add ---")
	ListContacts(phonebook)

	// Test: Delete existing contact
	phonebook, err = DeleteContact("Bob", phonebook)
	if err != nil {
		fmt.Println("Delete error:", err)
	}

	// Test: Delete non-existing contact
	phonebook, err = DeleteContact("Nobody", phonebook)
	if err != nil {
		fmt.Println("Delete error:", err)
	}

	fmt.Println("--- After Delete ---")
	ListContacts(phonebook)
}
