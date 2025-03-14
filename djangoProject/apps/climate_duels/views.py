from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from .models import ClimateDuel, Policy, PowerUp, PlayerPowerUp

@login_required
def create_duel(request):
    """Create a new climate duel and wait for an opponent."""
    duel = ClimateDuel.objects.create(player_one=request.user)
    messages.success(request, "Duel created! Waiting for an opponent...")
    return redirect("climate_duels:duel_list")

@login_required
def join_duel(request, duel_id):
    """Join an existing duel as Player Two and start the game."""
    duel = get_object_or_404(ClimateDuel, id=duel_id)

    # Ensure the duel is not already full (only one player is allowed to join)
    if duel.player_two is not None:
        messages.error(request, "This duel is already full!")
        return redirect("climate_duels:duel_list")

    if duel.player_one == request.user:
        messages.error(request, "You cannot join your own duel!")
        return redirect("climate_duels:duel_list")

    # Assign the second player and activate the duel
    duel.player_two = request.user
    duel.active = True  # Now activate the duel
    duel.save()

    messages.success(request, f"Joined duel against {duel.player_one.username}!")
    print(f"DEBUG: {request.user.username} successfully joined duel {duel.id}.")

    # Redirect to the first turn
    return redirect("climate_duels:play_turn", duel_id=duel.id)

def duel_list(request):
    """Show all duels, including those waiting for a second player."""
    duels = ClimateDuel.objects.all().order_by("-created_at")  # Show latest first
    return render(request, "climate_duels/duel_list.html", {"duels": duels})

@login_required
def duel_results(request, duel_id):
    """Displays the results of a completed duel."""
    duel = get_object_or_404(ClimateDuel, id=duel_id)

    # Determine the winner
    if duel.player_one_co2 <= 0 and duel.player_two_co2 <= 0:
        if duel.player_one_gdp > duel.player_two_gdp:
            winner = duel.player_one
        elif duel.player_two_gdp > duel.player_one_gdp:
            winner = duel.player_two
        else:
            winner = None  # Draw
    elif duel.player_one_co2 <= 0:
        winner = duel.player_one
    elif duel.player_two_co2 <= 0:
        winner = duel.player_two
    else:
        winner = None  # Fallback, should not happen

    return render(request, "climate_duels/duel_results.html", {"duel": duel, "winner": winner})


# Game logic

@login_required
def play_turn(request, duel_id):
    """Process a turn where a player selects policies, uses Power-Ups, and responds to events."""
    duel = get_object_or_404(ClimateDuel, id=duel_id)

    # Redirect to results page if the duel is over
    if not duel.active:
        return redirect("climate_duels:duel_results", duel_id=duel.id)

    # Ensure only the participating players can play
    if request.user not in [duel.player_one, duel.player_two]:
        messages.error(request, "You are not part of this duel.")
        return redirect("climate_duels:duel_list")

    # Determine whose turn it is
    is_player_one_turn = duel.current_turn % 2 == 1
    is_player_turn = (is_player_one_turn and request.user == duel.player_one) or \
                     (not is_player_one_turn and request.user == duel.player_two)

    if not is_player_turn:
        return render(request, "climate_duels/wait_turn.html", {"duel": duel})

    if request.method == "POST":
        policy_ids = request.POST.getlist("policy_ids")  # Allow up to two policies per turn
        powerup_id = request.POST.get("powerup_id")  # Check if a Power-Up is used
        action = request.POST.get("action")  # Check if a player decided to take a loan or pass

        # Check if there are any policies that cost 0 GDP
        free_policy_available = Policy.objects.filter(cost=0).exists()

        # Handle actions for players with no GDP
        if request.user == duel.player_one and duel.player_one_budget <= 0 and not free_policy_available:
            if action == "take_loan":
                duel.player_one_budget += 5
                duel.player_one_co2 += 2
                messages.success(request, "Emergency loan taken! +5 GDP, +2 CO₂.")
            elif action == "pass_turn":
                messages.info(request, "You passed your turn.")
                duel.current_turn += 1
                duel.save()
                return render(request, "climate_duels/wait_turn.html", {"duel": duel})
            else:
                messages.error(request, "Invalid action.")
                return redirect("climate_duels:play_turn", duel_id=duel.id)

        elif request.user == duel.player_two and duel.player_two_budget <= 0 and not free_policy_available:
            if action == "take_loan":
                duel.player_two_budget += 5
                duel.player_two_co2 += 2
                messages.success(request, "Emergency loan taken! +5 GDP, +2 CO₂.")
            elif action == "pass_turn":
                messages.info(request, "You passed your turn.")
                duel.current_turn += 1
                duel.save()
                return render(request, "climate_duels/wait_turn.html", {"duel": duel})
            else:
                messages.error(request, "Invalid action.")
                return redirect("climate_duels:play_turn", duel_id=duel.id)

        # Filter policies that the player can afford
        player_budget = duel.player_one_budget if request.user == duel.player_one else duel.player_two_budget
        affordable_policies = Policy.objects.filter(cost__lte=player_budget)

        # Ensure at least one policy is always selectable
        if not affordable_policies.exists():
            messages.warning(request, "You do not have enough GDP to afford any policies. You may need to pass your turn.")

        # Check if the player can afford policies
        if len(policy_ids) == 0 and affordable_policies.exists():
            messages.error(request, "You must select at least one policy if you can afford it.")
            return redirect("climate_duels:play_turn", duel_id=duel.id)
        elif len(policy_ids) == 0:
            messages.info(request, "No affordable policies available. You must pass your turn or take a loan.")
            return render(request, "climate_duels/pass_turn.html", {"duel": duel})

        policies = Policy.objects.filter(id__in=policy_ids)
        total_policy_cost = sum(p.cost for p in policies)
        total_gdp_impact = sum(p.gdp_impact for p in policies)

        # Ensure player has enough GDP to afford the policies
        if request.user == duel.player_one:
            if duel.player_one_budget < total_policy_cost:
                messages.error(request, "Not enough GDP to afford these policies!")
                return redirect("climate_duels:play_turn", duel_id=duel.id)
            duel.player_one_budget -= total_policy_cost
            duel.player_one_gdp += total_gdp_impact
        else:
            if duel.player_two_budget < total_policy_cost:
                messages.error(request, "Not enough GDP to afford these policies!")
                return redirect("climate_duels:play_turn", duel_id=duel.id)
            duel.player_two_budget -= total_policy_cost
            duel.player_two_gdp += total_gdp_impact

        # **💥 Handle Power-Ups**
        if powerup_id:
            player_powerup = get_object_or_404(PlayerPowerUp, id=powerup_id, user=request.user)
            powerup = player_powerup.powerup  # Get the associated PowerUp
            if powerup.effect_type == "co2_reduction":
                if request.user == duel.player_one:
                    duel.player_one_co2 -= powerup.effect_value
                else:
                    duel.player_two_co2 -= powerup.effect_value
            elif powerup.effect_type == "gdp_boost":
                if request.user == duel.player_one:
                    duel.player_one_gdp += powerup.effect_value
                else:
                    duel.player_two_gdp += powerup.effect_value

            if player_powerup.quantity > 1:
                player_powerup.quantity -= 1
                player_powerup.save()
            else:
                player_powerup.delete()     

        # Ensure an event is not triggered two turns in a row
        if not hasattr(duel, "event_processed") or not duel.event_processed:
            events = [
                {"name": "Global Heatwave", "co2_change": 5.0, "gdp_change": -2.0, "choice": True},
                {"name": "Renewable Energy Boom", "co2_change": -10.0, "gdp_change": 3.0, "choice": False},
                {"name": "Natural Disaster", "co2_change": -3.0, "gdp_change": -5.0, "choice": True},
                {"name": "Green Tech Breakthrough", "co2_change": -7.0, "gdp_change": 4.0, "choice": False}
            ]
            event = random.choice(events)
            
            # Store event in the duel object
            duel.event_processed = True
            duel.save()

            if event["choice"]:
                return render(request, "climate_duels/event_choice.html", {
                    "duel": duel,
                    "event": event,
                    "event_options": event.get("options", [])  # Ensure options are passed
                })

            # Apply automatic event effects
            duel.player_one_co2 += event["co2_change"]
            duel.player_one_gdp += event["gdp_change"]
            duel.player_two_co2 += event["co2_change"]
            duel.player_two_gdp += event["gdp_change"]

        # Reset event flag at the start of the next turn
        duel.event_processed = False
        duel.current_turn += 1
        duel.save()

        # **✅ Check for Win Conditions**
        if duel.player_one_co2 <= 0 and duel.player_two_co2 <= 0:
            if duel.player_one_gdp > duel.player_two_gdp:
                winner = duel.player_one
            elif duel.player_two_gdp > duel.player_one_gdp:
                winner = duel.player_two
            else:
                winner = None  # Draw
        elif duel.player_one_co2 <= 0:
            winner = duel.player_one
        elif duel.player_two_co2 <= 0:
            winner = duel.player_two
        else:
            winner = None

        if winner:
            duel.active = False
            duel.save()
            return redirect("climate_duels:duel_results", duel_id=duel.id)

        duel.save()
        messages.success(request, f"Turn played! {event['name']} occurred!")
        return render(request, "climate_duels/wait_turn.html", {"duel": duel, "event": event})

    # Filter policies that the player can afford
    player_budget = duel.player_one_budget if request.user == duel.player_one else duel.player_two_budget
    affordable_policies = Policy.objects.filter(cost__lte=player_budget)

    policies = Policy.objects.all()

    powerups = PlayerPowerUp.objects.filter(user=request.user).select_related('powerup')

    return render(request, "climate_duels/play_turn.html", {
        "duel": duel,
        "policies": policies,
        "powerups": powerups,
        "player_budget": duel.player_one_budget if request.user == duel.player_one else duel.player_two_budget,
    })
