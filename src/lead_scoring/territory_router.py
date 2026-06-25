"""Route leads to sales officers based on territory"""

from typing import Dict, List


class TerritoryRouter:
    """Route leads to appropriate sales officers"""
    
    def __init__(self, territory_config: Dict = None):
        """
        Initialize with territory configuration
        
        Args:
            territory_config: Dict mapping territories to officers
        """
        
        self.territory_config = territory_config or self._default_config()
    
    def _default_config(self) -> Dict:
        """Default territory configuration"""
        
        return {
            'West': {
                'states': ['Maharashtra', 'Gujarat', 'Goa'],
                'officers': [
                    {
                        'name': 'Rajesh Kumar',
                        'email': 'rajesh.kumar@hpcl.co.in',
                        'phone': '+91-9876543210',
                        'specialization': ['Steel', 'Power', 'Chemicals'],
                        'depot': 'Mumbai'
                    },
                    {
                        'name': 'Priya Shah',
                        'email': 'priya.shah@hpcl.co.in',
                        'phone': '+91-9876543211',
                        'specialization': ['Construction', 'Infrastructure'],
                        'depot': 'Ahmedabad'
                    }
                ]
            },
            'North': {
                'states': ['Delhi', 'Punjab', 'Haryana', 'Rajasthan', 'Uttar Pradesh'],
                'officers': [
                    {
                        'name': 'Amit Verma',
                        'email': 'amit.verma@hpcl.co.in',
                        'phone': '+91-9876543212',
                        'specialization': ['Manufacturing', 'Textiles'],
                        'depot': 'Delhi'
                    }
                ]
            },
            'East': {
                'states': ['West Bengal', 'Odisha', 'Bihar', 'Jharkhand'],
                'officers': [
                    {
                        'name': 'Amit Das',
                        'email': 'amit.das@hpcl.co.in',
                        'phone': '+91-9876543213',
                        'specialization': ['Jute', 'Steel', 'Mining'],
                        'depot': 'Kolkata'
                    }
                ]
            },
            'South': {
                'states': ['Tamil Nadu', 'Karnataka', 'Andhra Pradesh', 'Telangana', 'Kerala'],
                'officers': [
                    {
                        'name': 'Lakshmi Iyer',
                        'email': 'lakshmi.iyer@hpcl.co.in',
                        'phone': '+91-9876543214',
                        'specialization': ['Automotive', 'IT', 'Textiles'],
                        'depot': 'Chennai'
                    },
                    {
                        'name': 'Karthik Reddy',
                        'email': 'karthik.reddy@hpcl.co.in',
                        'phone': '+91-9876543215',
                        'specialization': ['Pharma', 'Chemicals'],
                        'depot': 'Hyderabad'
                    }
                ]
            }
        }
    
    def route_lead(
        self,
        location: str,
        industry: str = None,
        nearest_depot: str = None
    ) -> Dict:
        """
        Route lead to appropriate sales officer
        
        Args:
            location: Location string
            industry: Industry type (optional, for specialization matching)
            nearest_depot: Nearest depot (from proximity scorer)
        
        Returns:
            Dict with assigned officer details
        """
        
        # Determine region from location
        region = self._get_region(location)
        
        if not region:
            # Default to nearest depot's region
            region = self._get_region_from_depot(nearest_depot)
        
        # Get officers for region
        region_config = self.territory_config.get(region, self.territory_config['North'])
        officers = region_config['officers']
        
        # Match by specialization if industry provided
        if industry:
            for officer in officers:
                if any(spec.lower() in industry.lower() for spec in officer['specialization']):
                    return {
                        'assigned_officer': officer['name'],
                        'email': officer['email'],
                        'phone': officer['phone'],
                        'depot': officer['depot'],
                        'region': region,
                        'match_reason': f'Specialization match: {industry}'
                    }
        
        # Default: First officer in region
        officer = officers[0]
        return {
            'assigned_officer': officer['name'],
            'email': officer['email'],
            'phone': officer['phone'],
            'depot': officer['depot'],
            'region': region,
            'match_reason': 'Geographic assignment'
        }
    
    def _get_region(self, location: str) -> str:
        """Get region from location string"""
        
        if not location:
            return None
        
        location_lower = location.lower()
        
        for region, config in self.territory_config.items():
            for state in config['states']:
                if state.lower() in location_lower:
                    return region
        
        return None
    
    def _get_region_from_depot(self, depot: str) -> str:
        """Get region from depot name"""
        
        depot_regions = {
            'Mumbai': 'West', 'Ahmedabad': 'West', 'Pune': 'West',
            'Delhi': 'North', 'Jaipur': 'North',
            'Kolkata': 'East',
            'Chennai': 'South', 'Bangalore': 'South', 'Hyderabad': 'South'
        }
        
        return depot_regions.get(depot, 'North')