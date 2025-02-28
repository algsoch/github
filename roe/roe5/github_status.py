import requests
import datetime
import os
from getpass import getpass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import track
from rich import box

# GitHub OAuth Application credentials (kept for future use)
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:8000/callback"
AUTH_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"

# Initialize Rich console
console = Console()

def get_github_token():
    """Get GitHub token from environment variable or user input"""
    
    # First check for an environment variable
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        console.print("[bold green]Using GitHub token from environment variable[/bold green]")
        return token
    
    # Ask user to enter their token
    console.print(Panel.fit(
        "[bold]GitHub Authentication[/bold]\n\nPlease enter your GitHub Personal Access Token\n"
        "You can create one at [link=https://github.com/settings/tokens]https://github.com/settings/tokens[/link]\n"
        "Recommended scopes: [bold]repo[/bold], [bold]read:user[/bold]",
        title="Authentication Required",
        border_style="blue"
    ))
    token = getpass("Enter token (input will be hidden): ")
    
    if not token:
        console.print("[bold red]No token provided.[/bold red]")
        return None
    
    return token

def get_github_status(username, token=None):
    """Retrieve GitHub working status for a user."""
    
    # Set up session with authentication if token is provided
    session = requests.Session()
    if token:
        session.headers.update({'Authorization': f'token {token}'})
    
    # Show a loading message
    with console.status("[bold green]Fetching GitHub data...[/bold green]"):
        
        # Get basic user information
        user_url = f"https://api.github.com/users/{username}"
        user_response = session.get(user_url)
        
        if user_response.status_code != 200:
            console.print(f"[bold red]Error retrieving user data: {user_response.status_code}[/bold red]")
            return
            
        user_data = user_response.json()
        
        # Get repositories
        repos_url = f"https://api.github.com/users/{username}/repos"
        repos_response = session.get(repos_url)
        
        if repos_response.status_code != 200:
            console.print(f"[bold red]Error retrieving repository data: {repos_response.status_code}[/bold red]")
            return
            
        repos_data = repos_response.json()
        
        # Get recent activity (events)
        events_url = f"https://api.github.com/users/{username}/events/public"
        events_response = session.get(events_url)
        
        if events_response.status_code != 200:
            console.print(f"[bold red]Error retrieving activity data: {events_response.status_code}[/bold red]")
            return
            
        events_data = events_response.json()
        
        # Get contribution statistics (requires authentication)
        contributions = {}
        if token:
            # This endpoint requires authentication
            today = datetime.date.today()
            last_year = today - datetime.timedelta(days=365)
            stats_url = f"https://api.github.com/search/commits?q=author:{username}+author-date:>{last_year.isoformat()}"
            stats_response = session.get(stats_url, headers={"Accept": "application/vnd.github.cloak-preview"})
            
            if stats_response.status_code == 200:
                contributions = stats_response.json()
    
    # Display the results with Rich formatting
    
    # User profile section
    console.print("\n")
    profile_text = f"""# GitHub Profile: {user_data.get('name', username)} (@{username})

**Bio:** {user_data.get('bio', 'Not provided')}
**Location:** {user_data.get('location', 'Not provided')}
**Repositories:** {user_data['public_repos']} | **Followers:** {user_data['followers']} | **Following:** {user_data['following']}
**Member since:** {user_data['created_at'][:10]}
"""
    
    console.print(Panel(Markdown(profile_text), 
                       title="[bold blue]GitHub Profile[/bold blue]",
                       border_style="blue", 
                       expand=False))
    
    # Repositories section
    repo_table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    repo_table.add_column("Name", style="dim")
    repo_table.add_column("Description")
    repo_table.add_column("Language", style="green")
    repo_table.add_column("Stars", justify="right")
    repo_table.add_column("Forks", justify="right")
    repo_table.add_column("Last Updated")
    
    for repo in sorted(repos_data, key=lambda x: x['updated_at'], reverse=True)[:5]:
        repo_table.add_row(
            repo['name'],
            repo['description'] or 'No description',
            repo['language'] or 'Not specified',
            str(repo['stargazers_count']),
            str(repo['forks_count']),
            repo['updated_at'][:10]
        )
    
    console.print(Panel(repo_table, title="[bold cyan]Recent Repositories[/bold cyan]", border_style="cyan"))
    
    # Recent activity section
    activity_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    activity_table.add_column("Type", style="bold")
    activity_table.add_column("Repository")
    activity_table.add_column("Date")
    
    activity_types = {}
    for event in events_data[:10]:
        event_type = event['type'].replace('Event', '')
        repo_name = event['repo']['name']
        created_at = event['created_at'][:10]
        
        # Count event types
        if event_type in activity_types:
            activity_types[event_type] += 1
        else:
            activity_types[event_type] = 1
            
        activity_table.add_row(event_type, repo_name, created_at)
    
    console.print(Panel(activity_table, title="[bold magenta]Recent Activity[/bold magenta]", border_style="magenta"))
    
    # Activity summary section
    summary_table = Table(show_header=True, header_style="bold yellow", box=box.ROUNDED)
    summary_table.add_column("Activity Type")
    summary_table.add_column("Count", justify="right")
    
    for activity, count in activity_types.items():
        summary_table.add_row(activity, str(count))
    
    # Add commit count if available
    if contributions and 'total_count' in contributions:
        summary_table.add_row("Total Commits (Last Year)", str(contributions['total_count']))
    
    console.print(Panel(summary_table, title="[bold yellow]Activity Summary[/bold yellow]", border_style="yellow"))
    
    # Print footer
    console.print("\n[dim]Data retrieved from GitHub API on " + 
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/dim]")

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold blue]GitHub Status Dashboard[/bold blue]\n\n"
        "This tool shows your GitHub profile status, recent repositories, and activity.",
        border_style="blue"
    ))
    
    username = console.input("[bold]Enter your GitHub username:[/bold] ")
    
    # Use environment variable or manually entered token
    token = get_github_token()
    
    get_github_status(username, token)